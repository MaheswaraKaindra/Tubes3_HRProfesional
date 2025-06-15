# src/backend/search_logic.py

import re
from .levenshtein_distance import calculate_similarity

def find_fuzzy_matches(query: str, cv_text: str, threshold: float = 80.0) -> list[dict]:
    # Extract unique words from the CV text (Efficiency matters bozo)
    unique_words = set(re.findall(r'\b\w+\b', cv_text.lower()))
    found_matches = []

    for word in unique_words:
        similarity = calculate_similarity(query.lower(), word)

        if similarity >= threshold:
            found_matches.append({
                'word': word,
                'similarity': similarity
            })
    
    return sorted(found_matches, key=lambda x: x['similarity'])