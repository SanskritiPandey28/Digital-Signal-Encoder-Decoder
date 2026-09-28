import numpy as np

def generate_random_bits(length):
    bits = np.random.randint(0, 2, length)
    return ''.join(map(str, bits))