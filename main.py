
from data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    find_longest_palindrome
)

from line_coding import encode_nrz_l , encode_nrz_i

from plotting import (
    plot_digital_data,
    plot_line_signal
)


# ==========================================
# 1. Generate random digital data
# ==========================================

bits = generate_random_bits(20)

print("=" * 45)
print("1. RANDOM DIGITAL DATA")
print("=" * 45)

print("Generated bits:")
print(bits)

print("\nLongest palindromic substring:")
print(find_longest_palindrome(bits))

plot_digital_data(bits)


# ==========================================
# 2. Generate data with consecutive zeros
# ==========================================

bits_with_zeros = generate_bits_with_zeros(20, 8)

print("\n" + "=" * 45)
print("2. DATA WITH 8 CONSECUTIVE ZEROS")
print("=" * 45)

print("Generated bits:")
print(bits_with_zeros)

print("\nLongest palindromic substring:")
print(find_longest_palindrome(bits_with_zeros))


# ==========================================
# 3. NRZ-L line coding
# ==========================================

encoded_signal = encode_nrz_l(bits)

print("\n" + "=" * 45)
print("3. NRZ-L LINE CODING")
print("=" * 45)

print("Original digital data:")
print(bits)

print("\nNRZ-L encoded signal:")
print(encoded_signal)

plot_line_signal(encoded_signal, "NRZ-L Encoding")

# ==========================================
# 4. NRZ-I line coding
# ==========================================

encoded_nrz_i = encode_nrz_i(bits)

print("\n" + "=" * 45)
print("4. NRZ-I LINE CODING")
print("=" * 45)

print("Original digital data:")
print(bits)

print("\nNRZ-I encoded signal:")
print(encoded_nrz_i)

plot_line_signal(encoded_nrz_i, "NRZ-I Encoding")