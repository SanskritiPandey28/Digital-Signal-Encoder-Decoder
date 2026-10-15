
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
def plot_line_signal(signal, title="Line-Coded Signal"):
    if not signal:
        raise ValueError("Signal cannot be empty.")

    time = list(range(len(signal) + 1))
    levels = signal + [signal[-1]]

    plt.figure(figsize=(10, 4))
    plt.step(time, levels, where="post")

    plt.title(title)
    plt.xlabel("Time (bit intervals)")
    plt.ylabel("Signal level")

    plt.xticks(time)
    plt.yticks([-1, 0, 1])
    plt.ylim(-1.5, 1.5)
    plt.grid(True)

    plt.show()
