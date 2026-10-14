
from data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    find_longest_palindrome
)

from plotting import plot_digital_data

bits = generate_random_bits(20)

print("Random digital data:")
print(bits)


plot_digital_data(bits)

print("\nLongest palindromic substring:")
print(find_longest_palindrome(bits))

bits_with_zeros = generate_bits_with_zeros(20, 8)

print("\nDigital data with 8 consecutive zeros:")
print(bits_with_zeros)

print("\nLongest palindrome in this data:")
print(find_longest_palindrome(bits_with_zeros))
