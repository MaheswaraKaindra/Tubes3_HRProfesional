# src/backend/levenshtein_distance.py

import numpy as np

def levenshtein_distance(s1 : str, s2 : str) -> int:
    m, n = len(s1), len(s2)
    
    # Create (m+1) x (n+1) matrix
    dp = np.zeros((m + 1, n + 1), dtype=int)

    # Initialize the first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Compute the rest mwheehehehehe
    for i in range (1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,        # Deletion
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution
    return dp[m][n]

def calculate_similarity(s1 : str, s2 : str) -> float:
    # Just in case (the input should not be Null)
    if not s1 and not s2:
        return 0.0

    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return (1 - (distance / max_len)) * 100 if max_len > 0 else 0.0