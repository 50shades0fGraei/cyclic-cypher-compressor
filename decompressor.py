
import argparse
import sys
import os

from key import generate_cypher
import core.engine as engine

# --- CCC Decompressor Engine v11.0 ---

CHARACTER_SET = "abcdefghijklmnopqrstuvwxy"
CYCLIC_CONSTANT = "142857"

def parse_meta_file(meta_path):
    """Reads the .meta file and extracts the necessary information."""
    meta_info = {}
    with open(meta_path, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ', 1)
            if key == 'original_size_bytes':
                meta_info['original_size'] = int(value)
            elif key == 'compressed_signature':
                meta_info['signature'] = [int(v) for v in value.split(',')]
    return meta_info

def get_wait_time(char_to_find, stream, start_pos):
    """
    Calculates the 'wait time' for a character in a stream from a given position.
    This must be identical to the function in ccc-engine.py.
    """
    try:
        index = stream.index(char_to_find, start_pos)
        return index - start_pos
    except ValueError:
        return -1

def decompress(meta_path, output_path, secret_key):
    """
    Reconstructs the original file from a .meta signature file.
    """
    print(f"--- Starting CCC Decompressor v11.0 for: {meta_path} ---")

    meta_info = parse_meta_file(meta_path)
    original_size = meta_info['original_size']
    target_signature = meta_info['signature']
    print(f"1. Parsed .meta file. Original size: {original_size} bytes.")

    sovereign_variables = generate_cypher.generate_sovereign_variables(secret_key)
    shuffled_alphabets = engine.generate_shuffled_alphabets(sovereign_variables)
    rotor_streams = engine.generate_rotor_streams(shuffled_alphabets, original_size)
    cypher_pairs = [(rotor_streams[i], rotor_streams[i+6]) for i in range(6)]
    print("2. Re-generated cypher streams.")

    print("3. Beginning reconstruction...")
    reconstructed_content = []
    current_signature = [0] * 6

    # This is a complex backtracking search problem. The current implementation is a brute-force
    # approach, which will be very slow for large files. A more optimized algorithm
    # would be needed for practical use.
    
    # --- Pre-calculate all possible future costs ---
    # To make the search feasible, we need to know the total possible tally from a certain point onwards.
    # This is a placeholder for a much more complex calculation.
    
    memo = {}

    def find_char_for_position(pos, signature_at_pos):
        if pos == original_size:
            return [] if signature_at_pos == target_signature else None

        state = (pos, tuple(signature_at_pos))
        if state in memo:
            return memo[state]

        for char_to_test in CHARACTER_SET:
            temp_signature = list(signature_at_pos)
            
            for pair_index, (forward_rotor, reverse_rotor) in enumerate(cypher_pairs):
                forward_tally = get_wait_time(char_to_test, forward_rotor, pos)
                reverse_tally = get_wait_time(char_to_test, reverse_rotor, pos)
                
                total_pair_tally = 0
                if forward_tally != -1: total_pair_tally += forward_tally
                if reverse_tally != -1: total_pair_tally += reverse_tally
                temp_signature[pair_index] += total_pair_tally
            
            cyclic_digit = int(CYCLIC_CONSTANT[pos % len(CYCLIC_CONSTANT)])
            new_signature = [val + cyclic_digit for val in temp_signature]

            # Simple check: if any signature component exceeds the target, this path is wrong.
            # This is a vital pruning step.
            if any(ns > ts for ns, ts in zip(new_signature, target_signature)):
                continue

            result = find_char_for_position(pos + 1, new_signature)
            
            if result is not None:
                memo[state] = [char_to_test] + result
                return [char_to_test] + result
        
        memo[state] = None
        return None

    reconstructed_content = find_char_for_position(0, [0]*6)

    if reconstructed_content:
        final_content = "".join(reconstructed_content)
        print("\n4. Reconstruction successful!")
    else:
        final_content = "ERROR: Reconstruction failed. Could not find a valid path."
        print("\n4. Reconstruction failed.")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"5. Decompression finished. Output saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Decompressor Engine (v11.0).")
    parser.add_argument("--input", type=str, required=True, help="Path to the .meta file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the reconstructed file.")
    parser.add_argument("--key", type=str, required=True, help="The secret key used for compression.")
    args = parser.parse_args()

    decompress(args.input, args.output, args.key)
