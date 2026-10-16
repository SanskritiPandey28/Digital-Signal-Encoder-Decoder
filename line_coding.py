
# 1. NRZ-L Encoding
def encode_nrz_l(bits):
    mapping = {
        '0': -1,
        '1': 1
    }

    return [mapping[bit] for bit in bits]


# 2. NRZ-I Encoding
def encode_nrz_i(bits, initial_level=-1):
    signal = []
    current_level = initial_level

    for bit in bits:
        current_level *= (-1) ** int(bit)
        signal.append(current_level)

    return signal


# 3. Manchester Encoding
def encode_manchester(bits):
    mapping = {
        '0': [1, -1],
        '1': [-1, 1]
    }

    return [
        level
        for bit in bits
        for level in mapping[bit]
    ]


#Diffrential Manchester
def encode_differential_manchester(bits, initial_level=-1):
    signal = []
    current_level = initial_level

    for bit in bits:
        current_level *= (-1) ** (int(bit) == 0)
        signal.extend([current_level, -current_level])
        current_level = -current_level

    return signal
