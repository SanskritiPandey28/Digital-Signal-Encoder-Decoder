
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


# Pulse table used by AMI (and later by the scrambling schemes)
# symbol : (has_pulse, flips_polarity)
#   '0' -> no pulse, polarity unchanged
#   '1' -> pulse, polarity flips (normal AMI mark)
#   'B' -> pulse, polarity flips (bipolar pulse, follows the AMI rule)
#   'V' -> pulse, polarity NOT flipped (violation, same sign as last pulse)
PULSE_TABLE = {
    '0': (0, 0),
    '1': (1, 1),
    'B': (1, 1),
    'V': (1, 0)
}


def apply_pulses(symbols, initial_level=-1):
    signal = []
    current_level = initial_level

    for symbol in symbols:
        has_pulse, flips = PULSE_TABLE[symbol]
        current_level *= (-1) ** flips
        signal.append(has_pulse * current_level)

    return signal


# 5. AMI (Alternate Mark Inversion) Encoding
def encode_ami(bits):
    return apply_pulses(bits)


# 6. B8ZS Scrambling (Bipolar with 8-Zero Substitution)
# Every run of 8 zeros is replaced by 000VB0VB, then the
# pulse table turns V and B into the right voltages
def scramble_b8zs(bits):
    return apply_pulses(bits.replace('00000000', '000VB0VB'))
