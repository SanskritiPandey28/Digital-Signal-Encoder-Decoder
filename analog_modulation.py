
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
