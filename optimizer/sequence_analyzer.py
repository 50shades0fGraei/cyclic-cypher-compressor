
import os
import sys
from collections import Counter
import argparse

def find_frequent_sequences(input_path, n=2):
    """
    Analyzes the data section of a .ccc.opt file to find the most
    frequent sequences of symbols (n-grams).
    """
    archive_input_path = os.path.join("archive", input_path)
    print(f"\n1. Reading optimized file: '{archive_input_path}'")
    try:
        with open(archive_input_path, 'r', encoding='utf-8') as f:
            full_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Optimized file not found in archive.")
        sys.exit(1)

    try:
        # Isolate the data section
        _, data_part = full_content.split("\n---CCC_DATA---\n")
        symbols = data_part.strip().split(' ')
    except ValueError:
        print("ERROR: Optimized file is corrupt or has no data section.")
        sys.exit(1)

    print(f"2. Analyzing for {n}-gram sequences...")

    # Generate n-grams (sequences of n symbols)
    if len(symbols) < n:
        print("Not enough data to generate sequences.")
        return

    sequences = []
    for i in range(len(symbols) - n + 1):
        sequence = tuple(symbols[i:i+n])
        sequences.append(sequence)

    # Count the frequency of each sequence
    sequence_counts = Counter(sequences)

    print(f"\n--- Top 10 Most Frequent {n}-Gram Sequences ---")
    for (sequence, count) in sequence_counts.most_common(10):
        print(f"{count}: {' '.join(sequence)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Sequence Analyzer.")
    parser.add_argument("--input", type=str, required=True, help="The .ccc.opt file in /archive.")
    parser.add_argument("--n", type=int, default=2, help="The length of the sequence to analyze (e.g., 2 for bigrams, 3 for trigrams).")
    
    args = parser.parse_args()
    
    find_frequent_sequences(args.input, args.n)
