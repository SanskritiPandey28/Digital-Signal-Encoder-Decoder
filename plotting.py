
import matplotlib.pyplot as plt


def plot_digital_data(bits):
    # Convert each bit from a character to an integer
    bit_values = [int(bit) for bit in bits]

    # Time positions for the bit boundaries
    time = list(range(len(bit_values) + 1))

    # Repeat each bit value so it remains constant for one bit interval
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
