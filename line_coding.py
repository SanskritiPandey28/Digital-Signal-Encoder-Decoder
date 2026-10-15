
def encode_nrz_l(bits):
    signal = []

    for bit in bits:
        if bit == '1':
            signal.append(1)
        elif bit == '0':
            signal.append(-1)
        else:
            raise ValueError("Input must contain only 0s and 1s.")

    return signal


def encode_nrz_i(bits, initial_level=-1):
    signal = []
    current_level = initial_level

    for bit in bits:
        if bit == '1':
            current_level = -current_level
        elif bit != '0':
            raise ValueError("Input must contain only 0s and 1s.")

        signal.append(current_level)

    return signal
