
import argparse
import sys
import os

from key import generate_cypher
import core.engine as engine

# --- The Cyclic Cypher Compressor (CCC) Engine v11.0 ---
# This version performs the full compression, generating a final, fixed-size
# integer signature, proving the compression ratio.

CHARACTER_SET = "abcdefghijklmnopqrstuvwxy"
CYCLIC_CONSTANT = "142857"

def get_wait_time(char_to_find, stream, start_pos):
    try:
        index = stream.index(char_to_find, start_pos)
        return index - start_pos
    except ValueError:
        return -1

def transmute_and_compress(input_path, output_path, secret_key):
    print(f"--- Starting CCC FULL COMPRESSION Engine v11.0 for: {input_path} ---")

    sovereign_variables = generate_cypher.generate_sovereign_variables(secret_key)
    print("1. Generated sovereign variables.")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_path}")
        sys.exit(1)
    file_length = len(input_content)
    print(f"2. Read {file_length} characters from input file.")

    shuffled_alphabets = engine.generate_shuffled_alphabets(sovereign_variables)
    rotor_streams = engine.generate_rotor_streams(shuffled_alphabets, file_length)
    cypher_pairs = [(rotor_streams[i], rotor_streams[i+6]) for i in range(6)]
    print("3. Generated rotor streams and cypher pairs.")

    # --- The Core Compression ---
    # Instead of a trace, we sum the coordinates into a final integer.
    final_signature = [0] * 6
    literals = {}

    for i, char_original_case in enumerate(input_content):
        char = char_original_case.lower()

        if char not in CHARACTER_SET:
            if i not in literals:
                literals[i] = char_original_case
            continue

        for pair_index, (forward_rotor, reverse_rotor) in enumerate(cypher_pairs):
            forward_tally = get_wait_time(char, forward_rotor, i)
            reverse_tally = get_wait_time(char, reverse_rotor, i)
            
            total_pair_tally = 0
            if forward_tally != -1: total_pair_tally += forward_tally
            if reverse_tally != -1: total_pair_tally += reverse_tally
            
            final_signature[pair_index] += total_pair_tally
        
        cyclic_digit = int(CYCLIC_CONSTANT[i % len(CYCLIC_CONSTANT)])
        final_signature = [val + cyclic_digit for val in final_signature]

    print("4. Completed core compression.")

    signature_str = ",".join(map(str, final_signature))

    meta_content = f"input_file: {os.path.basename(input_path)}\n"
    meta_content += f"original_size_bytes: {file_length}\n"
    meta_content += f"compressed_signature: {signature_str}\n"
    meta_content += f"signature_size_bytes: {len(signature_str.encode('utf-8'))}\n"
    meta_content += f"compression_ratio: {(len(signature_str.encode('utf-8')) / file_length) * 100:.8f}%\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(meta_content)
    
    print(f"5. Full compression complete. Final signature saved to: {output_path}")
    print("\n--- RESULT ---")
    print(meta_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Full Compression Engine (v11.0).")
    parser.add_argument("--input", type=str, default="data/sample.txt")
    parser.add_argument("--output", type=str, default="data/sample.meta")
    args = parser.parse_args()
    transmute_and_compress(args.input, args.output, "default_key")
