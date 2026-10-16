
import matplotlib.pyplot as plt


# 1. Plot the original binary data
def plot_digital_data(bits):
    if not bits:
        raise ValueError("Digital data cannot be empty.")

    if any(bit not in "01" for bit in bits):
        raise ValueError("Input must contain only 0s and 1s.")

    bit_values = [int(bit) for bit in bits]

    time = list(range(len(bit_values) + 1))
    signal = bit_values + [bit_values[-1]]

    plt.figure(figsize=(10, 4))
    plt.step(time, signal, where="post")

    plt.title("Digital Data Signal")
    plt.xlabel("Time (bit intervals)")
    plt.ylabel("Bit value")

    plt.xticks(time)
    plt.yticks([0, 1])
    plt.ylim(-0.5, 1.5)
    plt.grid(True)

    plt.show()


# 2. Plot the encoded line signal

def plot_line_signal(
    signal,
    title="Line-Coded Signal",
    samples_per_bit=1
):
    if not signal:
        raise ValueError("Signal cannot be empty.")

    time = [
        i / samples_per_bit
        for i in range(len(signal) + 1)
    ]

    levels = signal + [signal[-1]]

    plt.figure(figsize=(10, 4))
    plt.step(time, levels, where="post")

    plt.title(title)
    plt.xlabel("Time (bit intervals)")
    plt.ylabel("Signal level")

    plt.yticks([-1, 0, 1])
    plt.ylim(-1.5, 1.5)
    plt.grid(True)

    plt.show()


# 3. Plot the analog signal, its samples and the PCM reconstruction
def plot_pcm(
    analog_time,
    analog_signal,
    sample_time,
    samples,
    decoded_samples
):
    plt.figure(figsize=(10, 4))

    plt.plot(analog_time, analog_signal, label="Analog signal")
    plt.stem(sample_time, samples, linefmt="C1-", markerfmt="C1o",
             basefmt=" ", label="Samples")
    plt.step(sample_time, decoded_samples, where="post",
             color="C2", label="PCM decoded (quantized)")

    plt.title("Pulse Code Modulation")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


# 4. Plot the analog signal with the Delta Modulation staircase
def plot_dm(
    analog_time,
    analog_signal,
    sample_time,
    staircase
):
    plt.figure(figsize=(10, 4))

    plt.plot(analog_time, analog_signal, label="Analog signal")
    plt.step(sample_time, staircase, where="post",
             color="C3", label="DM staircase (decoder output)")

    plt.title("Delta Modulation")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


# 5. Plot AMI before scrambling and after scrambling, one above the other
def plot_scrambling(ami_signal, scrambled_signal, scheme_name):
    time = list(range(len(ami_signal) + 1))

    figure, (top, bottom) = plt.subplots(
        2, 1, figsize=(10, 6), sharex=True
    )

    top.step(time, ami_signal + [ami_signal[-1]], where="post")
    top.set_title("AMI (before scrambling)")

    bottom.step(time, scrambled_signal + [scrambled_signal[-1]],
                where="post", color="C3")
    bottom.set_title(f"{scheme_name} (after scrambling)")
    bottom.set_xlabel("Time (bit intervals)")

    for axis in (top, bottom):
        axis.set_ylabel("Signal level")
        axis.set_yticks([-1, 0, 1])
        axis.set_ylim(-1.5, 1.5)
        axis.grid(True)

    figure.tight_layout()
    plt.show()
