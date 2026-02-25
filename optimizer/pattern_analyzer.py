
import os
import sys
from collections import Counter
import argparse

# --- CCC Pattern Analyzer (Optimizer) v1.1 ---

def analyze_and_optimize(input_path, output_path, threshold=5):
    """
    Reads a raw coordinate file (.ccc), finds the most frequent coordinate
    patterns, and generates a new, optimized file (.ccc.opt) with a codex.
    """
    archive_input_path = os.path.join("archive", input_path)
    print(f"\n1. Reading raw coordinate file: '{archive_input_path}'")
    try:
        with open(archive_input_path, 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: Raw coordinate file not found in archive.")
        sys.exit(1)

    coords = content.split(' ')
    
    print("2. Analyzing coordinate frequency to find common patterns...")
    coord_counts = Counter(coords)
    
    codex = {}
    # Use non-conflicting multi-character symbols for permanent letters
    next_perm_char_code = 0
    for coord, count in coord_counts.items():
        if count >= threshold:
            # Using simple base-62 style identifiers for robustness
            codex[coord] = f"p{next_perm_char_code}"
            next_perm_char_code += 1

    if not codex:
        print("No significant patterns found. Optimization may not be effective.")
        
    print(f"SUCCESS: Found {len(codex)} high-frequency patterns to optimize.")

    # --- Data Optimization ---
    # Create the new optimized data string, replacing patterns with permanent letters
    optimized_data_parts = []
    for coord in coords:
        if coord in codex:
            optimized_data_parts.append(codex[coord])
        else:
            # Raw coordinates are left as is. They contain a '-' which distinguishes them.
            optimized_data_parts.append(coord)
    
    # CRITICAL FIX: Join with spaces to create a parsable list.
    optimized_data = " ".join(optimized_data_parts)

    # --- File Assembly ---
    codex_string = ",".join([f"{v}:{k}" for k, v in codex.items()])
    final_content = f"---CCC_CODEX---\n{codex_string}\n---CCC_DATA---\n{optimized_data}"

    archive_output_path = os.path.join("archive", output_path)
    with open(archive_output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"3. Optimization complete. Saved to '{archive_output_path}'")
    
    original_size = os.path.getsize(archive_input_path)
    optimized_size = os.path.getsize(archive_output_path)
    reduction = ((original_size - optimized_size) / original_size) * 100 if original_size > 0 else 0
    print(f"\nOriginal Size: {original_size} bytes")
    print(f"Optimized Size:  {optimized_size} bytes")
    print(f"Reduction:       {reduction:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Pattern Analyzer and Optimizer.")
    parser.add_argument("--input", type=str, required=True, help="The raw .ccc coordinate file in /archive.")
    parser.add_argument("--output", type=str, required=True, help="The output .ccc.opt file name in /archive.")
    parser.add_argument("--threshold", type=int, default=5, help="Minimum frequency for a pattern to be added to the codex.")
    
    args = parser.parse_args()
    
    analyze_and_optimize(args.input, args.output, args.threshold)
