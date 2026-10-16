
import numpy as np

from data_generator import (
    generate_random_bits,
    generate_bits_with_zeros,
    find_longest_palindrome,
    find_longest_zero_run
)

from line_coding import (
    encode_nrz_l,
    encode_nrz_i,
    encode_manchester,
    encode_differential_manchester,
    encode_ami,
    scramble_b8zs,
    scramble_hdb3
)

from analog_modulation import (
    generate_analog_signal,
    sample_signal,
    pcm_encode,
    pcm_decode,
    dm_encode,
    dm_decode
)

from plotting import (
    plot_digital_data,
    plot_line_signal,
    plot_pcm,
    plot_dm,
    plot_scrambling
)


# ==========================================
# Input helpers
# ==========================================

# Show a numbered menu and return the value of the chosen option.
# Every menu in the program is a dictionary, so choosing an option
# is a dictionary lookup instead of a chain of if/else.
def ask_menu(title, options):
    print("\n" + title)

    for key, option in options.items():
        print("  " + key + ". " + option[0])

    while True:
        choice = input("Enter choice: ").strip()

        if choice in options:
            return options[choice]

        print("Invalid choice, try again.")


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()

        if answer in YES_NO:
            return YES_NO[answer]

        print("Please type y or n.")


def ask_number(prompt, default, cast=int, minimum=0):
    while True:
        text = input(prompt + " [default " + str(default) + "]: ").strip()

        try:
            value = cast(text or default)
        except ValueError:
            print("Please enter a number.")
            continue

        if value >= minimum:
            return value

        print("Value must be at least", minimum)


def ask_length():
    return ask_number("Number of bits", 20, int, 8)


def ask_own_bits():
    while True:
        bits = input("Enter your bits (only 0 and 1): ").strip()

        if bits != "" and set(bits) <= {'0', '1'}:
            return bits

        print("Only 0s and 1s are allowed.")


def print_heading(text):
    print("\n" + "=" * 45)
    print(text)
    print("=" * 45)


YES_NO = {
    'y': True,
    'yes': True,
    'n': False,
    'no': False
}


# ==========================================
# Menus (option : (name, action))
# ==========================================

def random_data():
    return generate_random_bits(ask_length())


def data_with_8_zeros():
    return generate_bits_with_zeros(ask_length(), 8)


def data_with_4_zeros():
    return generate_bits_with_zeros(ask_length(), 4)


DATA_SOURCES = {
    '1': ("Completely random data", random_data),
    '2': ("Random data with 8 consecutive zeros", data_with_8_zeros),
    '3': ("Random data with 4 consecutive zeros", data_with_4_zeros),
    '4': ("Enter my own bits", ask_own_bits)
}

SCRAMBLERS = {
    '1': ("B8ZS", scramble_b8zs),
    '2': ("HDB3", scramble_hdb3)
}


# ==========================================
# Scrambling (only offered after AMI)
# ==========================================

def run_scrambling(bits, ami_signal):
    name, scrambler = ask_menu("Choose scrambling type:", SCRAMBLERS)
    scrambled = scrambler(bits)

    print_heading(name + " SCRAMBLING")
    print("AMI signal before scrambling:")
    print(ami_signal)
    print("\n" + name + " scrambled signal:")
    print(scrambled)

    plot_scrambling(ami_signal, scrambled, name)


def offer_scrambling(bits, ami_signal):
    SCRAMBLE_ACTIONS[ask_yes_no("Do you want scrambling?")](bits, ami_signal)


def no_extra_step(bits, signal):
    pass


SCRAMBLE_ACTIONS = {
    True: run_scrambling,
    False: no_extra_step
}

# option : (name, encoder, samples per bit, step after encoding)
LINE_ENCODERS = {
    '1': ("NRZ-L", encode_nrz_l, 1, no_extra_step),
    '2': ("NRZ-I", encode_nrz_i, 1, no_extra_step),
    '3': ("Manchester", encode_manchester, 2, no_extra_step),
    '4': ("Differential Manchester",
          encode_differential_manchester, 2, no_extra_step),
    '5': ("AMI", encode_ami, 1, offer_scrambling)
}


# ==========================================
# Line coding (used by both digital and analog input)
# ==========================================

def run_line_coding(bits):
    print_heading("DIGITAL DATA")
    print("Digital data stream:")
    print(bits)
    print("\nLongest palindrome in the data stream:")
    print(find_longest_palindrome(bits))
    print("\nLongest run of consecutive zeros:")
    print(find_longest_zero_run(bits))

    plot_digital_data(bits)

    name, encoder, samples_per_bit, extra_step = ask_menu(
        "Choose line coding scheme:", LINE_ENCODERS
    )
    signal = encoder(bits)

    print_heading(name.upper() + " LINE CODING")
    print("Digital signal produced:")
    print(signal)

    plot_line_signal(signal, name + " Encoding", samples_per_bit)

    extra_step(bits, signal)


# ==========================================
# Digital input
# ==========================================

def digital_input():
    name, source = ask_menu("Choose how to generate the data:", DATA_SOURCES)

    run_line_coding(source())


# ==========================================
# Analog input (PCM / DM)
# ==========================================

def run_pcm(signal):
    n_bits = ask_number("Bits per sample", 3, int, 1)
    v_max = signal["amplitude"]

    bits, levels = pcm_encode(signal["samples"], n_bits, -v_max, v_max)
    decoded = pcm_decode(bits, n_bits, -v_max, v_max)

    print_heading("PCM ENCODER / DECODER")
    print("Samples:", np.round(signal["samples"], 3))
    print("Quantization levels:", levels)
    print("PCM bits:", bits)
    print("Decoded samples:", np.round(decoded, 3))

    plot_pcm(signal["analog_time"], signal["analog"],
             signal["sample_time"], signal["samples"], decoded)

    return bits


def run_dm(signal):
    # step that just keeps up with the steepest part of the sine wave
    suggested_delta = round(
        2 * np.pi * signal["frequency"] * signal["amplitude"]
        / signal["sampling_rate"], 3
    )
    delta = ask_number("Step size (delta)", suggested_delta, float, 0.001)

    bits, _ = dm_encode(signal["samples"], delta)
    staircase = dm_decode(bits, delta)

    print_heading("DELTA MODULATION ENCODER / DECODER")
    print("Samples:", np.round(signal["samples"], 3))
    print("DM bits:", bits)
    print("Staircase (decoder output):", np.round(staircase, 3))

    plot_dm(signal["analog_time"], signal["analog"],
            signal["sample_time"], staircase)

    return bits


ANALOG_TECHNIQUES = {
    '1': ("PCM (Pulse Code Modulation)", run_pcm),
    '2': ("DM (Delta Modulation)", run_dm)
}

NYQUIST_MESSAGE = {
    True: "Sampling rate satisfies the Nyquist rule (>= 2 x frequency).",
    False: "Warning: sampling rate is below 2 x frequency (Nyquist rule)."
}


def analog_input():
    amplitude = ask_number("Amplitude of the sine wave", 1.0, float, 0.1)
    frequency = ask_number("Frequency (Hz)", 1.0, float, 0.1)
    duration = ask_number("Duration (s)", 1.0, float, 0.1)
    sampling_rate = ask_number("Sampling rate (samples/s)", 16.0, float, 1)

    print(NYQUIST_MESSAGE[sampling_rate >= 2 * frequency])

    analog_time, analog = generate_analog_signal(
        amplitude, frequency, duration
    )
    sample_time, samples = sample_signal(
        amplitude, frequency, duration, sampling_rate
    )

    signal = {
        "amplitude": amplitude,
        "frequency": frequency,
        "sampling_rate": sampling_rate,
        "analog_time": analog_time,
        "analog": analog,
        "sample_time": sample_time,
        "samples": samples
    }

    name, technique = ask_menu("Choose technique:", ANALOG_TECHNIQUES)
    bits = technique(signal)

    print("\nThese bits are now passed to line coding.")
    run_line_coding(bits)


INPUT_TYPES = {
    '1': ("Digital input", digital_input),
    '2': ("Analog input (PCM / DM)", analog_input)
}


# ==========================================
# Main program
# ==========================================

def main():
    print_heading("DIGITAL SIGNAL ENCODER")

    keep_running = True

    while keep_running:
        name, run_input = ask_menu("Choose input type:", INPUT_TYPES)
        run_input()
        keep_running = ask_yes_no("\nRun again?")

    print("Goodbye!")


if __name__ == "__main__":
    main()
