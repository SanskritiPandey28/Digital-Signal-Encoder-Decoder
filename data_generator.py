
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


def find_longest_palindrome(bits):
    n = len(bits)

    if n == 0:
        return ""

    longest = ""

    for center in range(n):
        # Odd-length palindrome
        left = center
        right = center

        while (
            left >= 0
            and right < n
            and bits[left] == bits[right]
        ):
            if right - left + 1 > len(longest):
                longest = bits[left:right + 1]

            left -= 1
            right += 1

        # Even-length palindrome
        left = center
        right = center + 1

        while (
            left >= 0
            and right < n
            and bits[left] == bits[right]
        ):
            if right - left + 1 > len(longest):
                longest = bits[left:right + 1]

            left -= 1
            right += 1

    return longest