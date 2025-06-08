# src/backend/knuth_morris_pratt.py

from pdf_to_string import pdf_to_string 

def compute_border_function(pattern: str) -> list[int]:
    # Compute the border function for the Knuth-Morris-Pratt algorithm (size of the largest prefix which is also a suffix)
    # Returns a list[int] (just like PPT)

    m = len(pattern)

    # Initialize the border array with zeros
    border_array = [0] * m
    j = 0  # Length of the previous longest prefix suffix (the value that will be filled in border_array[i])
    i = 1  # Loop index for filling border_array[i]

    while i < m:
        if pattern[i] == pattern[j]:
            # Characters match
            j += 1
            border_array[i] = j
            i += 1
        else:
            if j != 0:
                # If there is a mismatch after j matches, use the previous border value
                j = border_array[j - 1]
            else:
                # If there is no match, set border_array[i] to 0 and move to the next character
                border_array[i] = 0
                i += 1
    return border_array

def knuth_morris_pratt(text: str, pattern: str) -> list[int]:
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return []
    
    border_array = compute_border_function(pattern)
    found_indexes = []
    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            # Match found
            found_indexes.append(i - j)
            j = border_array[j - 1]
        
        # Mismatch handling
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = border_array[j - 1]
            else:
                # No match, increment i
                i += 1
                
    return found_indexes

# Just for testing
if __name__ == "__main__":
    pdf_path = "10276858.pdf"
    text = pdf_to_string(pdf_path)
    pattern = "Consistently"
    found_indexes = knuth_morris_pratt(text, pattern)
    if found_indexes:
        print(f"Pattern '{pattern}' found at indexes: {found_indexes}")
    else:
        print(f"Pattern '{pattern}' not found in the text.")
    print("Text length:", len(text))
    print("Pattern length:", len(pattern))
    print("Found indexes length:", len(found_indexes))