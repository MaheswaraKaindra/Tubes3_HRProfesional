# src/backend/search_controller.py

import os
import time

# Imports
from .pdf_to_string import pdf_to_string, normalize_text
from .knuth_morris_pratt import knuth_morris_pratt
from .boyer_moore import boyer_moore

_cv_data_cache = []

def load_cv_data(directory: str):
    global _cv_data_cache
    if _cv_data_cache: return
    print (f"Loading CV data from directory: {directory}")
    temp_cv_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            print (f"Processing file: {file}")
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                raw_text = pdf_to_string(file_path)

                if raw_text:
                    normalized_text = normalize_text(raw_text)
                    temp_cv_data.append({
                        'path': file_path,
                        'name': os.path.splitext(file)[0],
                        'raw_text': raw_text,
                        'normalized_text': normalized_text
                    })
    _cv_data_cache = temp_cv_data
    print(f"Loaded {len(_cv_data_cache)} CVs from {directory}")

def search_cv_data(keywords: list[str], algorithm: str) -> dict:
    start_time = time.perf_counter()

    if algorithm == 'KMP':
        search_function = knuth_morris_pratt
    elif algorithm == 'BM':
        search_function = boyer_moore

    all_results = []
    for cv in _cv_data_cache:
        keyword_counts = {}
        matched_keywords = 0

        for keyword in keywords:
            keyword = keyword.strip().lower()
            if not keyword:
                continue

            found_indexes = search_function(cv['normalized_text'], keyword)
            if found_indexes:
                keyword_counts[keyword.strip()] = len(found_indexes)
                matched_keywords += 1
    
        if matched_keywords > 0:
            all_results.append({
                'name': cv['name'],
                'path': cv['path'],
                'keyword_counts': keyword_counts,
                'matched_keywords': matched_keywords,
            })
    
    sorted_results = sorted(all_results, key=lambda x: x['matched_keywords'], reverse=True)
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000

    return {
        'results': sorted_results,
        'scan_count': len(_cv_data_cache),
        'execution_time': execution_time
    }