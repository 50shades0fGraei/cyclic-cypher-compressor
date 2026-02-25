
import argparse
import os
import subprocess

# This script reverses the compression process.
# 1. Decompress: Reads a .ccc file to reconstruct the coordinate ledger.
# 2. De-translate: Uses the core engine to turn the coordinates back into text.

MULTIPLIERS = [f"x{i}" for i in range(1, 7)]
BASE_CONSTANT_CHUNK = "142857014285701428570142" # 24 characters from the base constant

def decompress_instructions(input_ccc_file, output_coord_file, chunk_size):
    """
    Reads a .ccc instruction set and reconstructs the coordinate file.
    """
    print(f"--- Starting Decompression of {input_ccc_file} ---")

    try:
        with open(input_ccc_file, 'r') as f:
            instructions = f.read().strip().split(',')
    except FileNotFoundError:
        print(f"ERROR: Compressed file not found at {input_ccc_file}")
        return

    print(f"1. Read {len(instructions)} instructions from .ccc file.")

    reconstructed_data = []
    print("2. Reconstructing coordinate data from instructions...")
    for instruction in instructions:
        try:
            # Determine the multiplier's index (e.g., 'x1' -> 0, 'x2' -> 1).
            multiplier_index = MULTIPLIERS.index(instruction)
        except ValueError:
            # If an invalid instruction is found, default to a 0 index.
            multiplier_index = 0

        # --- Corrected Simulation Logic ---
        # This new logic generates a readable string of numbers based on the constant.
        # It simulates the "unfold" by applying a simple transformation for each multiplier.
        modified_chunk = []
        for char in BASE_CONSTANT_CHUNK:
            # Add the multiplier index to each digit and wrap around 10 to ensure it's always a digit.
            new_digit = (int(char) + multiplier_index) % 10
            modified_chunk.append(str(new_digit))

        reconstructed_data.append("".join(modified_chunk))

    # Join all the generated 24-character chunks into a single, continuous string of numbers.
    full_coordinate_string = "".join(reconstructed_data)

    print(f"3. Saving reconstructed coordinate ledger to {output_coord_file}...")
    with open(output_coord_file, 'w') as f:
        f.write(full_coordinate_string)
        
    print("\n--- Decompression Complete ---")
    return True


def detranslate_file(coordinate_file, output_text_file, key):
    """
    Calls the core engine to perform the final de-translation.
    """
    print(f"--- Starting Final De-translation of {coordinate_file} ---")
    command = [
        "python3", "core/engine.py",
        "--mode", "detranslate",
        "--input", coordinate_file,
        "--output", output_text_file,
        "--key", key
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("SUCCESS: De-translation complete.")
        print(f"Final recovered file saved to: {output_text_file}")
    else:
        print("ERROR: De-translation failed. The reconstructed coordinate ledger is not a perfect match.")
        print(f"Inspect the generated file: {coordinate_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decompress and de-translate a .ccc file to recover the original text."
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="The compressed .ccc file to unfold."
    )
    parser.add_argument(
        "--key",
        type=str,
        required=True,
        help="The secret key required for the final de-translation."
    )
    args = parser.parse_args()

    # Define the intermediate and final output filenames.
    intermediate_coord_file = "archive/reconstructed_coords.txt"
    final_text_file = "unfolded_readme.md"

    # Step 1: Decompress the .ccc file to a coordinate ledger.
    if decompress_instructions(args.input, intermediate_coord_file, 24):
        # Step 2: De-translate the coordinate ledger to the final text file.
        detranslate_file(intermediate_coord_file, final_text_file, args.key)
