
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


# 5. AMI (Alternate Mark Inversion) Encoding
# 0 -> zero voltage, 1 -> a pulse that alternates between +1 and -1
def encode_ami(bits):
    signal = []
    last_pulse = -1   # so that the first '1' becomes +1

    for bit in bits:
        if bit == '1':
            last_pulse = -last_pulse
            signal.append(last_pulse)
        else:
            signal.append(0)

    return signal
