
import numpy as np


# ==========================================
# Analog input
# ==========================================

# A smooth sine wave (used only for drawing the "real" analog signal)
def generate_analog_signal(amplitude, frequency, duration, points=1000):
    time = np.linspace(0, duration, points)
    return time, amplitude * np.sin(2 * np.pi * frequency * time)


# Take samples of the sine wave at regular moments
# (Nyquist: sampling_rate should be at least 2 x frequency)
def sample_signal(amplitude, frequency, duration, sampling_rate):
    time = np.arange(0, duration, 1 / sampling_rate)
    return time, amplitude * np.sin(2 * np.pi * frequency * time)


# ==========================================
# PCM (Pulse Code Modulation)
# ==========================================

# 1. Quantize each sample to one of 2^n levels
# 2. Write the level number in binary using n bits
def pcm_encode(samples, n_bits, v_min, v_max):
    levels = 2 ** n_bits
    step = (v_max - v_min) / levels

    level_index = np.floor((samples - v_min) / step)
    level_index = np.clip(level_index, 0, levels - 1).astype(int)

    bits = ''.join(
        format(index, f'0{n_bits}b')
        for index in level_index
    )

    return bits, level_index


# Read the bits back n at a time, turn each group into a level
# number, and place the value in the middle of that level
def pcm_decode(bits, n_bits, v_min, v_max):
    levels = 2 ** n_bits
    step = (v_max - v_min) / levels

    level_index = np.array([
        int(bits[i:i + n_bits], 2)
        for i in range(0, len(bits), n_bits)
    ])

    return v_min + (level_index + 0.5) * step


# ==========================================
# DM (Delta Modulation)
# ==========================================

# Send 1 bit per sample:
#   1 -> the signal is above our staircase, so step UP by delta
#   0 -> the signal is below our staircase, so step DOWN by delta
def dm_encode(samples, delta, initial_level=0.0):
    bits = []
    staircase = []
    current_level = initial_level

    for sample in samples:
        bit = int(sample > current_level)
        current_level += delta * (2 * bit - 1)    # 1 -> +delta, 0 -> -delta
        bits.append(str(bit))
        staircase.append(current_level)

    return ''.join(bits), np.array(staircase)


# Rebuild the staircase from the bits alone:
# every 1 adds +delta and every 0 adds -delta
def dm_decode(bits, delta, initial_level=0.0):
    steps = np.array([2 * int(bit) - 1 for bit in bits])
    return initial_level + delta * np.cumsum(steps)
