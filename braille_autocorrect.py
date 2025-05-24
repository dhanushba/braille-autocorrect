# braille_autocorrect.py
# Braille Autocorrect and Suggestion System for Thinkerbell Labs

from typing import List, Tuple
import heapq

# QWERTY Braille mapping
qwerty_to_dot = {'D': 1, 'W': 2, 'Q': 3, 'K': 4, 'O': 5, 'P': 6}

# Sample dictionary
dictionary = ['cat', 'cap', 'can', 'bat', 'ban', 'bad', 'dad', 'map', 'man', 'cab']

# Braille patterns for a-z
braille_encoding = {
    'a': [1], 'b': [1,2], 'c': [1,4], 'd': [1,4,5], 'e': [1,5], 'f': [1,2,4],
    'g': [1,2,4,5], 'h': [1,2,5], 'i': [2,4], 'j': [2,4,5], 'k': [1,3], 'l': [1,2,3],
    'm': [1,3,4], 'n': [1,3,4,5], 'o': [1,3,5], 'p': [1,2,3,4], 'q': [1,2,3,4,5],
    'r': [1,2,3,5], 's': [2,3,4], 't': [2,3,4,5], 'u': [1,3,6], 'v': [1,2,3,6],
    'w': [2,4,5,6], 'x': [1,3,4,6], 'y': [1,3,4,5,6], 'z': [1,3,5,6]
}

def text_to_braille(word: str) -> List[List[int]]:
    return [braille_encoding[c] for c in word if c in braille_encoding]

def qwerty_to_braille(char: List[str]) -> List[int]:
    return sorted([qwerty_to_dot[k] for k in char if k in qwerty_to_dot])

def word_to_qwerty_braille(word: str) -> List[List[int]]:
    return [sorted(braille_encoding[c]) for c in word if c in braille_encoding]

def levenshtein(a: List[List[int]], b: List[List[int]]) -> int:
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[m][n]

def suggest(word_input: List[List[str]], k: int = 3) -> List[str]:
    input_braille = [qwerty_to_braille(ch) for ch in word_input]
    heap = []
    for word in dictionary:
        b = word_to_qwerty_braille(word)
        dist = levenshtein(input_braille, b)
        heapq.heappush(heap, (dist, word))
    return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]

# Example usage
if __name__ == "__main__":
    user_input = [['D', 'K'], ['D'], ['W', 'Q', 'O']]
    suggestions = suggest(user_input)
    print("Suggestions:", suggestions)
