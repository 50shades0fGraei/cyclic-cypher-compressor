
import os
import sys
from collections import Counter
import argparse

# --- CCC Meta-Optimizer v1.0 ---

def meta_optimize(input_path, output_path, n=3, threshold=5):
    """
    Reads a .ccc.opt file, finds frequent sequences (n-grams), and
    creates a new, meta-optimized file (.ccc.final) with a second-level codex.
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
        header, data_part = full_content.split("\n---CCC_DATA---\n")
        symbols = data_part.strip().split(' ')
    except ValueError:
        print("ERROR: Optimized file is corrupt.")
        sys.exit(1)

    # --- Sequence Analysis ---
    print(f"2. Analyzing for {n}-gram sequences to meta-optimize...")
    sequences = []
    for i in range(len(symbols) - n + 1):
        sequence = tuple(symbols[i:i+n])
        sequences.append(sequence)

    sequence_counts = Counter(sequences)
    
    # --- Meta-Codex Generation ---
    meta_codex = {}
    # Use a new set of identifiers for the meta-symbols
    next_meta_char_code = 0
    for sequence, count in sequence_counts.items():
        if count >= threshold:
            meta_codex[" ".join(sequence)] = f"m{next_meta_char_code}"
            next_meta_char_code += 1

    if not meta_codex:
        print("No significant sequences found. Meta-optimization not performed.")
        sys.exit(0)

    print(f"SUCCESS: Found {len(meta_codex)} high-frequency sequences.")

    # --- Data Meta-Optimization ---
    print("3. Applying meta-compression...")
    # This is a simple, greedy replacement strategy.
    # For a perfect implementation, this would need to be more sophisticated
    # to handle overlapping sequences, but this will prove the concept.
    new_data_string = data_part.strip()
    for seq_str, meta_sym in meta_codex.items():
        new_data_string = new_data_string.replace(seq_str, meta_sym)

    # --- Final File Assembly ---
    meta_codex_string = ",".join([f"{v}:{k}" for k, v in meta_codex.items()])
    
    # We preserve the original codex and add the new one.
    final_content = f"{header}\n---CCC_META_CODEX---\n{meta_codex_string}\n---CCC_FINAL_DATA---\n{new_data_string}"

    archive_output_path = os.path.join("archive", output_path)
    with open(archive_output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"4. Meta-optimization complete. Saved to '{archive_output_path}'")

    # Compare file sizes
    original_size = os.path.getsize(archive_input_path)
    final_size = os.path.getsize(archive_output_path)
    reduction = ((original_size - final_size) / original_size) * 100 if original_size > 0 else 0
    print(f"\nOriginal Optimized Size: {original_size} bytes")
    print(f"Final Meta-Optimized Size: {final_size} bytes")
    print(f"Further Reduction:         {reduction:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Meta-Optimizer.")
    parser.add_argument("--input", type=str, required=True, help="The .ccc.opt file to meta-optimize.")
    parser.add_argument("--output", type=str, required=True, help="The output .ccc.final file name.")
    parser.add_argument("--n", type=int, default=3, help="The n-gram size to target.")
    parser.add_argument("--threshold", type=int, default=5, help="Minimum frequency for a sequence to be included in the meta-codex.")
    
    args = parser.parse_args()
    
    meta_optimize(args.input, args.output, args.n, args.threshold)
