# core/compressor.py
import json
import argparse
from itertools import cycle

# --- Constants ---
VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxz"
VOWEL_CYPHER_STRING = "142857"
CONSONANT_CYPHER_STRING = "1428570"

# --- Library Loading ---
def load_syllable_library(path="key/syllable_library.txt"):
    """Loads the syllable library from a file, longest first for greedy matching."""
    try:
        with open(path, "r") as f:
            return sorted([line.strip() for line in f if line.strip()], key=len, reverse=True)
    except FileNotFoundError:
        print(f"Error: Syllable library not found at '{path}'. Please ensure the file exists.")
        exit(1)

# --- Mapping Generation ---
def get_vowel_consonant_pattern(syllable):
    """Generates a V/C pattern for a syllable."""
    pattern = ""
    for char in syllable.lower():
        if char in VOWELS:
            pattern += "V"
        else:
            pattern += "C"
    return pattern

def create_letter_cyphers():
    """Creates C1 cypher maps for vowels and consonants."""
    vowel_map = {}
    consonant_map = {}
    vowel_cypher_sequence = cycle(VOWEL_CYPHER_STRING)
    for letter in VOWELS:
        vowel_map[letter] = int(next(vowel_cypher_sequence))
    consonant_cypher_sequence = cycle(CONSONANT_CYPHER_STRING)
    for letter in CONSONANTS:
        consonant_map[letter] = int(next(consonant_cypher_sequence))
    return vowel_map, consonant_map

def create_syllable_cypher_map(syllable_library, vowel_map, consonant_map):
    """Creates the C2 master map for all syllables with unique IDs."""
    cypher_map = {}
    sorted_syllables = sorted(list(set(syllable_library)))
    for i, syllable in enumerate(sorted_syllables):
        base_value = i
        pattern = get_vowel_consonant_pattern(syllable)
        letter_values = []
        for char in syllable:
            if char in VOWELS:
                letter_values.append(vowel_map.get(char, 0))
            else:
                letter_values.append(consonant_map.get(char, 0))
        multiplied_values = {}
        for j in range(1, 7):
            multiplied_values[f"x{j}"] = base_value * j
        syllable_data = {
            "type": "C2", "pattern": pattern, "base_value": base_value,
            "letter_values": letter_values, "multipliers": multiplied_values,
        }
        cypher_map[syllable] = syllable_data
    return cypher_map

# --- Core Logic ---
def compress(text, c2_map, c1_vowel_map, c1_consonant_map, syllable_library):
    """Compresses text, handling words, spaces, newlines, and case preservation."""
    compressed_data = []
    # Preserve structure by splitting on spaces but keeping newlines to be handled separately
    lines = text.split('\n')
    for line_idx, line in enumerate(lines):
        words = line.split(' ')
        for word_idx, word in enumerate(words):
            if not word: continue
            temp_word = word.lower()
            original_word = word
            original_idx = 0
            while len(temp_word) > 0:
                found_syllable = False
                for syllable in syllable_library:
                    if temp_word.startswith(syllable):
                        if syllable in c2_map:
                            # Preserve case information from original word
                            original_syllable = original_word[original_idx:original_idx + len(syllable)]
                            case_pattern = [1 if c.isupper() else 0 for c in original_syllable]
                            compressed_data.append({
                                "type": "C2",
                                **c2_map[syllable],
                                "case": case_pattern
                            })
                        temp_word = temp_word[len(syllable):]
                        original_idx += len(syllable)
                        found_syllable = True
                        break
                if not found_syllable:
                    char = temp_word[0]
                    original_char = original_word[original_idx]
                    if char in c1_vowel_map: value = c1_vowel_map[char]
                    elif char in c1_consonant_map: value = c1_consonant_map[char]
                    else: value = -1
                    compressed_data.append({
                        "type": "C1",
                        "char": char,
                        "value": value,
                        "is_uppercase": original_char.isupper()
                    })
                    temp_word = temp_word[1:]
                    original_idx += 1
            if word_idx < len(words) - 1:
                compressed_data.append({"type": "SPACE"})
        if line_idx < len(lines) - 1:
            compressed_data.append({"type": "NEWLINE"}) 
    return compressed_data

def decompress(compressed_data, c2_map, original_c2_map=None):
    """Decompresses a list of data blocks back into text, preserving case."""
    reconstructed_parts = []
    
    # Build reverse map: compare just the core C2 data (without type/case)
    reverse_c2_map = {}
    for syllable, c2_data in c2_map.items():
        # Store the mapping using the core C2 data structure
        reverse_c2_map[syllable] = c2_data
    
    for block in compressed_data:
        block_type = block.get("type")
        if block_type == "C1":
            char = block["char"]
            if block.get("is_uppercase", False):
                char = char.upper()
            reconstructed_parts.append(char)
        elif block_type == "C2":
            # Search through c2_map to find the matching syllable
            found_syllable = None
            for syllable, c2_data in c2_map.items():
                # Check if all keys in c2_data match the corresponding keys in block
                match = True
                for key, value in c2_data.items():
                    if key not in block or block[key] != value:
                        match = False
                        break
                if match:
                    found_syllable = syllable
                    break
            
            if found_syllable:
                # Apply case pattern if present
                case_pattern = block.get("case", [])
                syllable = found_syllable
                if case_pattern:
                    syllable_list = list(syllable)
                    for i, should_upper in enumerate(case_pattern):
                        if i < len(syllable_list):
                            syllable_list[i] = syllable_list[i].upper() if should_upper else syllable_list[i]
                    syllable = "".join(syllable_list)
                reconstructed_parts.append(syllable)
        elif block_type == "SPACE":
            reconstructed_parts.append(" ")
        elif block_type == "NEWLINE":
            reconstructed_parts.append("\n")
    return "".join(reconstructed_parts)

# --- Main Execution (CLI) ---
def main():
    parser = argparse.ArgumentParser(description="A tool for syllable-based text compression.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Compress Command ---
    parser_compress = subparsers.add_parser("compress", help="Compress a text file.")
    parser_compress.add_argument("--input", required=True, help="Path to the input text file.")
    parser_compress.add_argument("--output", required=True, help="Path for the output compressed file.")

    # --- Decompress Command ---
    parser_decompress = subparsers.add_parser("decompress", help="Decompress a file.")
    parser_decompress.add_argument("--input", required=True, help="Path to the compressed input file.")
    parser_decompress.add_argument("--output", required=True, help="Path for the output decompressed text file.")

    args = parser.parse_args()

    # --- Load Libraries and Maps ---
    syllable_library = load_syllable_library()
    vowel_cypher_map, consonant_cypher_map = create_letter_cyphers()
    master_cypher_map = create_syllable_cypher_map(syllable_library, vowel_cypher_map, consonant_cypher_map)

    # --- Execute Command ---
    if args.command == "compress":
        try:
            with open(args.input, 'r') as f:
                text_content = f.read()
            compressed_data = compress(text_content, master_cypher_map, vowel_cypher_map, consonant_cypher_map, syllable_library)
            with open(args.output, 'w') as f:
                json.dump(compressed_data, f, indent=2)
            print(f"Successfully compressed '{args.input}' to '{args.output}'.")
        except FileNotFoundError:
            print(f"Error: Input file not found at '{args.input}'.")

    elif args.command == "decompress":
        try:
            with open(args.input, 'r') as f:
                compressed_data = json.load(f)
            reconstructed_text = decompress(compressed_data, master_cypher_map)
            with open(args.output, 'w') as f:
                f.write(reconstructed_text)
            print(f"Successfully decompressed '{args.input}' to '{args.output}'.")
        except FileNotFoundError:
            print(f"Error: Input file not found at '{args.input}'.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{args.input}'. Is it a valid compressed file?")

if __name__ == "__main__":
    main()
