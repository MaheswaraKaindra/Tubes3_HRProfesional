# src/backend/search_controller.py

import os
import time
from .pdf_to_string import pdf_to_string, normalize_text
from .knuth_morris_pratt import knuth_morris_pratt
from .boyer_moore import boyer_moore
from .search_logic import find_fuzzy_matches

_cv_data_cache = []

import concurrent.futures

def process_pdf(file_tuple):
    # All imports must be inside for multiprocessing compatibility
    from .pdf_to_string import pdf_to_string, normalize_text
    import os
    file, file_path = file_tuple
    print(f"Processing file: {file}")
    raw_text = pdf_to_string(file_path)
    if raw_text:
        return {
            'path': file_path,
            'name': os.path.splitext(file)[0],
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

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_pdf, pdf_files))
        _cv_data_cache.extend([r for r in results if r is not None])

    print(f"Loaded {len(_cv_data_cache)} CVs.")

def search_cv_data(keywords: list[str], algorithm: str, top_n: int, fuzzy_threshold: float = 80.0) -> dict:
    start_time = time.perf_counter()
    search_function = knuth_morris_pratt if algorithm == 'KMP' else boyer_moore
    clean_keywords = {k.strip().lower() for k in keywords if k.strip()}
    
    import concurrent.futures

    def process_cv(cv):
        current_cv_keyword_counts = {}
        current_cv_matched_keywords = set()
        keywords_to_fuzzy_check = set(clean_keywords)

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
        if keywords_to_fuzzy_check:
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

    all_cv_results = []
    total_exact_time = 0
    total_fuzzy_time = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_cv, _cv_data_cache))
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