# src/backend/boyer_moore.py

from pdf_to_string import pdf_to_string

def compute_last_occurrence(pattern: str) -> dict:
    last_occurrence = {}
    for i, char in enumerate(pattern):
        last_occurrence[char] = i
    return last_occurrence

def boyer_moore(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return []
    
    last_occurrence = compute_last_occurrence(pattern)
    found_indexes = []

    # Start searching from the end of the pattern
    i = m - 1

    while i < n:
        # Pattern index
        j = m - 1

        # Comparation index
        k = i

        while j >= 0 and text[k] == pattern[j]:
            j -= 1
            k -= 1

        if j < 0:
            # Match found
            found_indexes.append(k + 1)
            # Shift the pattern to the right by the length of the pattern
            i += 1

        else:
            # Mismatch found, Character-Jump
            mismatched_char = text[i]
            temp_last_occurrence = last_occurrence.get(mismatched_char, -1)

            # Calculate the shift based on the last occurrence of the mismatched character
            shift = max(1, j - temp_last_occurrence)
            i += shift
    return found_indexes

# Just for testing
if __name__ == "__main__":
    pdf_path = "10276858.pdf"
    text = pdf_to_string(pdf_path)
    pattern = "Consistently"
    found_indexes = boyer_moore(text, pattern)
    if found_indexes:
        print(f"Pattern '{pattern}' found at indexes: {found_indexes}")
    else:
        print(f"Pattern '{pattern}' not found in the text.")
    print("Text length:", len(text))
    print("Pattern length:", len(pattern))
    print("Found indexes count:", len(found_indexes))