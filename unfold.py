
import argparse
import sys
import os
import struct

from key import generate_cypher
from core import engine
from sweeper import syllable_generator

# --- BitReader for parsing compact binary files ---
class BitReader:
    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.byte_index = 0
        self.bit_position = 0

    def read_bit(self):
        """Reads a single bit from the stream."""
        if self.byte_index >= len(self.byte_data):
            raise EOFError("End of stream reached")
        
        byte = self.byte_data[self.byte_index]
        bit = (byte >> (7 - self.bit_position)) & 1
        self.bit_position += 1

        if self.bit_position == 8:
            self.bit_position = 0
            self.byte_index += 1
            
        return bit

    def read(self, num_bits):
        """Reads a specified number of bits."""
        value = 0
        for _ in range(num_bits):
            value = (value << 1) | self.read_bit()
        return value

    def read_vint(self):
        """Reads a variable-length integer (VLQ) from the stream."""
        value = 0
        while True:
            byte = self.read(8)
            value = (value << 7) | (byte & 0x7f)
            if (byte & 0x80) == 0:
                break
        return value

# --- CCC Unfold Engine v1.2 ---
# This version reads the compact binary instruction set created by v8.5 of the engine.

def unfold_file(input_path, output_path, secret_key):
    """
    Reads a binary CCC instruction set and reconstructs the original file.
    """
    print(f"--- Starting CCC Unfold Engine v1.2 for: {input_path} ---")

    # 1. Read the Instruction Set and Header
    try:
        with open(input_path, 'rb') as f:
            # Read and verify header
            header = f.readline()
            if header != b'CCCv8.5\n':
                print(f"ERROR: Invalid file format. Expected CCCv8.5, got {header.decode()}")
                sys.exit(1)
            
            # Read file length
            file_length_bytes = f.read(4)
            file_length = struct.unpack('>I', file_length_bytes)[0]
            
            # Read the rest of the file for the BitReader
            compressed_data = f.read()
            reader = BitReader(compressed_data)

    except FileNotFoundError:
        print(f"ERROR: Instruction set file not found at {input_path}")
        sys.exit(1)

    print(f"1. Read instructions. Original file length: {file_length}.")

    # 2. Re-generate the exact same 12 Asynchronous Rotors
    sovereign_variables = generate_cypher.generate_sovereign_variables(secret_key)
    base_offset = int(sovereign_variables[0], 16) % 10 + 1
    
    forward_rotors = engine.generate_forward_overlays(
        syllable_generator.CYCLIC_CONSTANT, file_length, base_offset, step_rate=2
    )
    reverse_rotors = engine.generate_reverse_overlays(
        syllable_generator.CYCLIC_CONSTANT, file_length, base_offset, step_rate=1
    )
    all_rotors = forward_rotors + reverse_rotors
    print("2. Re-generated 12 key-specific asynchronous rotors with correct length.")

    # 3. Reconstruct the original data by following the instructions
    print("3. Reconstructing data from binary instruction set...")
    output_content = []
    current_pos = 0
    try:
        while current_pos < file_length:
            instruction_type = reader.read_bit() # Read 1 bit to determine type

            if instruction_type == 0: # LITERAL
                char_code = reader.read(8)
                output_content.append(chr(char_code))
                current_pos += 1
            else: # RUN
                run_length = reader.read_vint()
                for i in range(run_length):
                    pos_in_run = current_pos + i
                    char_found = False
                    for rotor in all_rotors:
                        if pos_in_run < len(rotor) and rotor[pos_in_run] != ' ':
                            output_content.append(rotor[pos_in_run])
                            char_found = True
                            break
                    if not char_found:
                        print(f"ERROR: Desynchronization at position {pos_in_run}. No character found.")
                        output_content.append("?")
                current_pos += run_length
    except EOFError:
        # This is expected when we've read all the data
        pass

    print("   - Reconstruction complete.")

    # 4. Write the reconstructed data to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("".join(output_content))

    print(f"4. Unfold complete. Reconstructed file saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Unfold Engine for the CCC (v1.2).")
    parser.add_argument("--input", type=str, default="archive/instruction_set.ccc")
    parser.add_-argument("--output", type=str, default="archive/unfolded_data.txt")
    parser.add_argument("--key", type=str, default="test")
    args = parser.parse_args()

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    unfold_file(args.input, args.output, args.key)
