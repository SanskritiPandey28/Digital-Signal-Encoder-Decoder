
import numpy as np


def generate_random_bits(length):
    bits = np.random.randint(0, 2, length)
    return ''.join(map(str, bits))


def generate_bits_with_zeros(length, zero_count):
    if length <= 0:
        raise ValueError("Length must be positive.")

    if zero_count < 1 or zero_count > length:
        raise ValueError("zero_count must be between 1 and length.")

    bits = np.random.randint(0, 2, length)

    start = np.random.randint(0, length - zero_count + 1)
    bits[start:start + zero_count] = 0

    return ''.join(map(str, bits))


# Longest palindrome using Manacher's algorithm - O(n)
def find_longest_palindrome(bits):
    # Put '#' between characters so odd and even palindromes
    # are handled the same way. '^' and '$' stop the expansion
    # at both ends without needing bounds checks.
    t = '^#' + '#'.join(bits) + '#$'
    n = len(t)

    p = [0] * n        # p[i] = palindrome radius around position i
    center = 0
    right = 0          # rightmost edge reached by any palindrome so far

    for i in range(1, n - 1):
        mirror = 2 * center - i

        # Reuse the mirror's answer (only inside the known palindrome)
        p[i] = max(0, min(right - i, p[mirror]))

        # Try to expand further
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        # Move the window if this palindrome reaches further right
        right, center = max((right, center), (i + p[i], i))

    best_length = max(p)
    best_center = p.index(best_length)
    start = (best_center - 1 - best_length) // 2

    return bits[start:start + best_length]
