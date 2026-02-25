
import sys
import os
import argparse
import hashlib
import struct

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sweeper.syllable_generator import FULL_LIBRARY, CYCLIC_CONSTANT

# --- CCC "Wait & Advance" Engine v7.1 ---

class BitWriter:
    def __init__(self):
        self.buffer = bytearray()
        self.current_byte = 0
        self.bit_position = 0

    def write(self, value, num_bits):
        for i in range(num_bits - 1, -1, -1):
            bit = (value >> i) & 1
            self.current_byte = (self.current_byte << 1) | bit
            self.bit_position += 1
            if self.bit_position == 8:
                self.buffer.append(self.current_byte)
                self.current_byte = 0
                self.bit_position = 0
    
    # New method to write variable-length integers for tally
    def write_vint(self, value):
        while True:
            byte = value & 0x7F
            value >>= 7
            if value == 0:
                self.write(byte, 8)
                break
            else:
                self.write(byte | 0x80, 8)

    def get_bytes(self):
        if self.bit_position > 0:
            self.current_byte <<= (8 - self.bit_position)
            self.buffer.append(self.current_byte)
        return self.buffer

class BitReader:
    # ... (BitReader remains the same for now)
    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.byte_index = 0
        self.bit_position = 0

    def read(self, num_bits):
        value = 0
        for _ in range(num_bits):
            if self.bit_position == 8:
                self.bit_position = 0
                self.byte_index += 1
            if self.byte_index >= len(self.byte_data):
                raise EOFError("Not enough bits to read.")
            byte = self.byte_data[self.byte_index]
            bit = (byte >> (7 - self.bit_position)) & 1
            value = (value << 1) | bit
            self.bit_position += 1
        return value

def _shuffle_list(char_list, sv_int):
    n = len(char_list)
    shuffled_list = char_list[:]
    for i in range(n - 1, 0, -1):
        cyclic_digit = int(CYCLIC_CONSTANT[i % len(CYCLIC_CONSTANT)])
        j = (sv_int + i * cyclic_digit) % (i + 1)
        shuffled_list[i], shuffled_list[j] = shuffled_list[j], shuffled_list[i]
    return shuffled_list

def generate_speed_variables(secret_key, count=6):
    hasher = hashlib.sha512()
    hasher.update(secret_key.encode('utf-8'))
    hex_hash = hasher.hexdigest()
    variables = []
    for i in range(count):
        start = i * 10
        end = start + 10
        variables.append(hex_hash[start:end])
    return variables

def compress_file(input_path, output_path, secret_key):
    print(f"\n1. Reading source file: '{input_path}'")
    with open(input_path, 'r', encoding='utf-8') as f: content = f.read()

    print("2. Generating Phantom Rotors from secret key...")
    speed_variables = generate_speed_variables(secret_key)
    phantoms = [_shuffle_list(FULL_LIBRARY, int(sv, 16)) for sv in speed_variables]
    
    heads = [0] * 6
    multipliers = [i + 1 for i in range(6)]
    lib_len = len(FULL_LIBRARY)

    print("3. Compressing with 'Wait & Advance' Engine (v7.1)...")
    writer = BitWriter()
    
    char_index = 0
    while char_index < len(content):
        char = content[char_index]
        if char not in FULL_LIBRARY:
            char_index += 1
            continue

        tally = 0
        found_match = False
        while not found_match:
            for i in range(len(phantoms)):
                if phantoms[i][heads[i]] == char:
                    # Found alignment! Write the instruction.
                    writer.write_vint(tally) # How many advances it took
                    writer.write(i, 3)       # Which phantom (multiplier)
                    
                    # Advance all heads one last time for this character
                    for j in range(len(heads)):
                        advance = int(CYCLIC_CONSTANT[heads[j] % len(CYCLIC_CONSTANT)]) * multipliers[j]
                        heads[j] = (heads[j] + advance) % lib_len
                    
                    found_match = True
                    break # Exit the inner for-loop
            
            if not found_match:
                # No match found, advance all heads and tally it
                tally += 1
                for i in range(len(heads)):
                    advance = int(CYCLIC_CONSTANT[heads[i] % len(CYCLIC_CONSTANT)]) * multipliers[i]
                    heads[i] = (heads[i] + advance) % lib_len
        
        char_index += 1 # Move to the next character

    compressed_data = writer.get_bytes()
    original_char_count = len(content)

    archive_output_path = os.path.join("archive", output_path)
    with open(archive_output_path, 'wb') as f:
        f.write(struct.pack('>I', original_char_count))
        f.write(compressed_data)

    print(f"SUCCESS: Alignment instructions saved to '{archive_output_path}'")
    original_size = os.path.getsize(input_path)
    final_size = os.path.getsize(archive_output_path)
    # Note: Reduction is not expected at this stage.
    print(f"\nOriginal Size: {original_size} bytes")
    print(f"Instruction File Size: {final_size} bytes")


def decompress_file(input_path, output_path, secret_key):
    # Decompression logic is now out of date and will be updated next.
    print("Decompression logic for v7.1 has not been implemented yet.")
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC 'Wait & Advance' Engine v7.1")
    parser.add_argument("mode", choices=["compress", "decompress"])
    parser.add_argument("--key", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.mode == "compress":
        compress_file(args.input, args.output, args.key)
    elif args.mode == "decompress":
        decompress_file(args.input, args.output, args.key)
