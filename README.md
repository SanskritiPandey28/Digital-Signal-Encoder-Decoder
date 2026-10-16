# Digital Signal Encoder

ITT 036 – Programming Assignment 1 (Data Communication)

A Python program that generates digital data (or samples an analog signal),
encodes it with different line coding schemes, and plots every signal.

## Features

- **Digital data generator** – completely random bits, random bits with
  8 or 4 consecutive zeros, or your own bits
- **Longest palindrome** in the data stream – Manacher's algorithm, O(n)
- **Longest run of consecutive zeros** – O(n)
- **Line coding** – NRZ-L, NRZ-I, Manchester, Differential Manchester, AMI
- **Scrambling** (offered after AMI) – B8ZS and HDB3, O(n)
- **Analog input** – sine wave sampled at a chosen rate (with a Nyquist check)
  - **PCM** encoder and decoder (quantization to 2^n levels)
  - **Delta Modulation** encoder and staircase decoder
  - The bits produced by PCM/DM are passed on to line coding
- **Plots** – digital data, line-coded signal, PCM reconstruction,
  DM staircase, AMI before/after scrambling

## Project structure

| File | Contents |
|---|---|
| `main.py` | Interactive menu – run this file |
| `data_generator.py` | Random data, longest palindrome, longest zero run |
| `line_coding.py` | NRZ-L, NRZ-I, Manchester, Differential Manchester, AMI, B8ZS, HDB3 |
| `analog_modulation.py` | Sine wave, sampling, PCM and DM encoder/decoder |
| `plotting.py` | All graphs (matplotlib) |
| `requirements.txt` | Python libraries used |

## Requirements

- Python 3.10 or newer
- numpy, matplotlib (listed in `requirements.txt`)

## How to run

```bash
# 1. create and activate a virtual environment (first time only)
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. install the libraries (first time only)
pip install -r requirements.txt

# 3. run the program
python main.py
```

Each graph opens in its own window – close it to continue the program.
Pressing Enter at a number prompt uses the default value shown in brackets.

## Example session

```
Choose input type:
  1. Digital input
  2. Analog input (PCM / DM)
Enter choice: 1

Choose how to generate the data:
  1. Completely random data
  2. Random data with 8 consecutive zeros
  ...
Enter choice: 2
Number of bits [default 20]:

Digital data stream:  10110000000011010010
Longest palindrome in the data stream:  ...
Longest run of consecutive zeros:  8

Choose line coding scheme: ... 5. AMI
Enter choice: 5
Do you want scrambling? (y/n): y
Choose scrambling type: 1. B8ZS  2. HDB3
```

## Assumptions

- Signal levels are +1 / 0 / −1 (normalised voltages).
- NRZ-L: 1 → +1, 0 → −1. NRZ-I: a 1 inverts the level (starting level −1).
- Manchester (IEEE 802.3): 0 → high-to-low, 1 → low-to-high.
- Differential Manchester: always a transition in the middle; an extra
  transition at the start of the bit for 0.
- AMI, B8ZS and HDB3: the "previous pulse" before the first 1 is taken
  as −1, so the first 1 becomes +1.
- HDB3 counts the pulses since the last substitution (odd → 000V, even → B00V).
- Analog input is a sine wave. PCM quantizes the range −A to +A into 2^n equal
  levels and reconstructs at the middle of each level. DM starts at level 0.

## Design notes

- Menus and scheme selection use dictionaries that map the user's choice to a
  function, instead of long if/else chains.
- AMI, B8ZS and HDB3 share one pulse table: each symbol (`0`, `1`, `B`, `V`)
  says whether it is a pulse and whether it flips the polarity. Scrambling only
  replaces zero runs with `B`/`V` symbols before the table is applied.

## References

- B. A. Forouzan, *Data Communications and Networking*, McGraw-Hill
  (Ch. 4: Digital Transmission)
- G. Manacher, "A New Linear-Time On-Line Algorithm for Finding the Smallest
  Initial Palindrome of a String", *Journal of the ACM*, 1975
- NumPy and Matplotlib documentation

## Team

- Sanskriti Pandey
- Poornima Joshi

## Acknowledgements

AI assistance (Claude by Anthropic) was used for explanations of the concepts
and for help with parts of the implementation, as required to be acknowledged
by the assignment.
