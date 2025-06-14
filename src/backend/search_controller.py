# src/backend/search_controller.py

import os
import time
import mysql.connector
from .knuth_morris_pratt import knuth_morris_pratt
from .boyer_moore import boyer_moore
from .search_logic import find_fuzzy_matches
from .aho_corasick import aho_corasick

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="hr_admin",
            password="",
            database="HRProfesional_schema"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
    
def get_path_to_name_map():
    path_map = {}
    connection = get_db_connection()
    if not connection: return path_map
    
    cursor = connection.cursor()
    query = """
    SELECT 
        p.first_name, 
        p.last_name, 
        d.cv_path 
    FROM 
        ApplicantProfile p 
    JOIN 
        ApplicationDetail d ON p.applicant_id = d.applicant_id
    WHERE 
        d.cv_path IS NOT NULL;
    """
    try:
        cursor.execute(query)
        for first_name, last_name, cv_path in cursor.fetchall():
            normalized_path = cv_path.replace('\\', '/').lower()
            path_map[normalized_path] = f"{first_name} {last_name}"
    except mysql.connector.Error as e:
        print(f"Error fetching names from DB: {e}")
    finally:
        cursor.close()
        connection.close()
    return path_map

_cv_data_cache = []

import concurrent.futures

def process_pdf(file_tuple):
    # All imports must be inside for multiprocessing compatibility
    from .pdf_to_string import pdf_to_string, normalize_text
    import os
    file, file_path = file_tuple
    print(f"Processing file: {file}")
    raw_text = pdf_to_string(file_path)
    name_map = get_path_to_name_map()
    try:
        data_index = file_path.lower().rindex('data/')
        relative_path = file_path[data_index:].replace('\\', '/').lower()
    except ValueError:
        relative_path = file_path.replace('\\', '/').lower()
    db_name = name_map.get(relative_path)
    if raw_text:
        return {
            'path': file_path,
            'name': db_name if db_name else os.path.splitext(file)[0],
            'raw_text': raw_text,
            'normalized_text': normalize_text(raw_text)
        }
    return None

def load_cv_data(directory: str):
    global _cv_data_cache
    if _cv_data_cache:
        return
    print(f"Loading CV data from directory: {directory}")

    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                pdf_files.append((file, file_path))

    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
        results = list(executor.map(process_pdf, pdf_files))
        _cv_data_cache.extend([r for r in results if r is not None])

    print(f"Loaded {len(_cv_data_cache)} CVs.")

def process_cv(cv, clean_keywords, algorithm, fuzzy_threshold):
    if algorithm == 'KMP':
        search_function = knuth_morris_pratt
    elif algorithm == 'BM':
        search_function = boyer_moore
    elif algorithm == 'AC':
        search_function = None  # handled separately WKWKWK formatnya beda
    else:
        search_function = knuth_morris_pratt
    current_cv_keyword_counts = {}
    current_cv_matched_keywords = set()
    keywords_to_fuzzy_check = set(clean_keywords)

    if algorithm == 'AC':
        ac_results = aho_corasick(cv['normalized_text'], list(clean_keywords))
        for keyword, count in ac_results.items():
            if count > 0:
                current_cv_keyword_counts[keyword] = count
                current_cv_matched_keywords.add(keyword)
                if keyword in keywords_to_fuzzy_check:
                    keywords_to_fuzzy_check.remove(keyword)
        exact_time = 0
    else:
        exact_start = time.perf_counter()
        for keyword in clean_keywords:
            print(f"Processing keyword: '{keyword}' in CV: '{cv['name']}'")
            matches = search_function(cv['normalized_text'], keyword)
            if matches:
                current_cv_keyword_counts[keyword] = len(matches)
                current_cv_matched_keywords.add(keyword)
                if keyword in keywords_to_fuzzy_check:
                    keywords_to_fuzzy_check.remove(keyword)
        exact_time = time.perf_counter() - exact_start

    fuzzy_time = 0
    if keywords_to_fuzzy_check and algorithm != 'AC':
        fuzzy_start = time.perf_counter()
        for keyword in keywords_to_fuzzy_check:
            print(f"Processing fuzzy keyword: '{keyword}' in CV: '{cv['name']}'")
            fuzzy_matches = find_fuzzy_matches(keyword, cv['normalized_text'], fuzzy_threshold)
            if fuzzy_matches:
                best_match_word = fuzzy_matches[0]['word']
                frequency_of_best_match = len(search_function(cv['normalized_text'], best_match_word))
                match_key = f"{keyword} → {best_match_word}"
                current_cv_keyword_counts[match_key] = frequency_of_best_match
                current_cv_matched_keywords.add(keyword)
        fuzzy_time = time.perf_counter() - fuzzy_start

    if current_cv_matched_keywords:
        return {
            'name': cv['name'],
            'path': cv['path'],
            'keyword_counts': current_cv_keyword_counts,
            'relevance_score': len(current_cv_matched_keywords),
            'exact_time': exact_time,
            'fuzzy_time': fuzzy_time
        }
    else:
        return None

def _process_cv_wrapper(args):
    cv, clean_keywords, algorithm, fuzzy_threshold = args
    return process_cv(cv, clean_keywords, algorithm, fuzzy_threshold)

def search_cv_data(keywords: list[str], algorithm: str, top_n: int, fuzzy_threshold: float = 80.0) -> dict:
    start_time = time.perf_counter()
    clean_keywords = {k.strip().lower() for k in keywords if k.strip()}

    all_cv_results = []
    total_exact_time = 0
    total_fuzzy_time = 0

    import concurrent.futures
    # Prepare arguments for each CV
    args_list = [(cv, clean_keywords, algorithm, fuzzy_threshold) for cv in _cv_data_cache]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(_process_cv_wrapper, args_list))
        for res in results:
            if res is not None:
                all_cv_results.append(res)
                total_exact_time += res.get('exact_time', 0)
                total_fuzzy_time += res.get('fuzzy_time', 0)

    sorted_results = sorted(all_cv_results, key=lambda x: x['relevance_score'], reverse=True)
    print(f"Found {len(sorted_results)} CVs matching the keywords.")

    return {
        'results': sorted_results,
        'scan_count': len(_cv_data_cache),
        'exact_time': total_exact_time * 1000,
        'fuzzy_time': total_fuzzy_time * 1000
    }