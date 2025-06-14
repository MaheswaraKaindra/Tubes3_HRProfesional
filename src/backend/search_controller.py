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

    exact_results = {}
    keywords_with_no_exact_match = set(clean_keywords)

    for cv in _cv_data_cache:
        cv_path = cv['path']
        current_cv_matches = {}
        for keyword in clean_keywords:
            matches = search_function(cv['normalized_text'], keyword)
            if matches:
                current_cv_matches[keyword] = len(matches)
                if keyword in keywords_with_no_exact_match:
                    keywords_with_no_exact_match.remove(keyword)
        
        if current_cv_matches:
            exact_results[cv_path] = {
                'name': cv['name'], 'path': cv['path'],
                'keyword_counts': current_cv_matches,
                'relevance_score': len(current_cv_matches)
            }
    
    exact_match_time = (time.perf_counter() - start_time) * 1000

    sorted_exact_results = sorted(exact_results.values(), key=lambda x: x['relevance_score'], reverse=True)

    final_results = sorted_exact_results
    fuzzy_match_time = 0.0

    needs_fuzzy_search = bool(keywords_with_no_exact_match) or (len(final_results) < top_n)
    
    if needs_fuzzy_search:
        fuzzy_start_time = time.perf_counter()
        
        exact_result_paths = {res['path'] for res in final_results}
        cvs_for_fuzzy = [cv for cv in _cv_data_cache if cv['path'] not in exact_result_paths]
        
        keywords_for_fuzzy = clean_keywords.union(keywords_with_no_exact_match)

        fuzzy_results = {}
        for cv in cvs_for_fuzzy:
            cv_path = cv['path']
            current_cv_fuzzy_matches = {}
            for keyword in keywords_for_fuzzy:
                matches = find_fuzzy_matches(keyword, cv['normalized_text'], fuzzy_threshold)
                if matches:
                    match_key = f"{keyword} (fuzzy)"
                    best_match = matches[0]
                    current_cv_fuzzy_matches[match_key] = f"{best_match['word']} ({best_match['similarity']:.1f}%)"
            
            if current_cv_fuzzy_matches:
                fuzzy_results[cv_path] = {
                    'name': cv['name'], 'path': cv['path'],
                    'keyword_counts': current_cv_fuzzy_matches,
                    'relevance_score': len(current_cv_fuzzy_matches)
                }
        
        sorted_fuzzy_results = sorted(fuzzy_results.values(), key=lambda x: x['relevance_score'], reverse=True)
        
        if len(final_results) < top_n:
            needed = top_n - len(final_results)
            final_results.extend(sorted_fuzzy_results[:needed])

        fuzzy_match_time = (time.perf_counter() - fuzzy_start_time) * 1000

    return {
        'results': final_results,
        'scan_count': len(_cv_data_cache),
        'exact_time': exact_match_time,
        'fuzzy_time': fuzzy_match_time
    }