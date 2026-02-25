
import argparse
import string

# --- The "Braid" Architecture: Complete, Case-Sensitive Character Sets ---

# "Breath" contains all vowels, now including uppercase.
BREATH_CHARS = list("aeiouyAEIOUY")

# "Punctuation" is the definitive set of all non-alphanumeric symbols.
TYPOGRAPHIC_SYMBOLS = "‘’“”"
EM_DASH = "—"
PUNCTUATION_CHARS = list(string.punctuation + TYPOGRAPHIC_SYMBOLS + EM_DASH + "\n" + "\t")

# "Frame" is for all other characters: consonants (upper and lower), numbers, and the space character.
CONSONANTS = "bcdfghjklmnpqrstvwxz"
NUMBERS_AND_SPACE = string.digits + " "
FRAME_CHARS = list(CONSONANTS + CONSONANTS.upper() + NUMBERS_AND_SPACE)

# --- The "Nonmoving Phantom": The Complete, Ordered Character Library ---
# This single list is the ground state, the "Ideal Set" for the entire system.
FULL_LIBRARY = FRAME_CHARS + BREATH_CHARS + PUNCTUATION_CHARS


# The core cyclic constant of the engine.
CYCLIC_CONSTANT = "1428570"

def _shuffle_list(char_list, sv_int):
    """
    A deterministic, self-contained shuffle algorithm that uses the Sovereign
    Variable integer and the cyclic constant to reorder a given list.
    """
    n = len(char_list)
    shuffled_list = char_list[:]
    for i in range(n - 1, 0, -1):
        cyclic_digit = int(CYCLIC_CONSTANT[i % len(CYCLIC_CONSTANT)])
        j = (sv_int + i * cyclic_digit) % (i + 1)
        shuffled_list[i], shuffled_list[j] = shuffled_list[j], shuffled_list[i]
    return shuffled_list

def generate_braided_slot(sovereign_variable):
    """
    Generates a "braided" cypher slot, consisting of two deterministically
    shuffled lists: one for FRAME characters and one for BREATH characters.
    """
    try:
        sv_int = int(sovereign_variable, 16)
    except ValueError:
        sv_int = sum(ord(c) for c in sovereign_variable)

    # Shuffle both the Frame and Breath lists using the same core logic.
    shuffled_frame = _shuffle_list(FRAME_CHARS, sv_int)
    shuffled_breath = _shuffle_list(BREATH_CHARS, sv_int)

    # The complete slot is a dictionary containing both shuffled lists.
    return {"frame": shuffled_frame, "breath": shuffled_breath}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a braided cypher slot or show the full library."
    )
    parser.add_argument(
        "--variable", type=str, help="One of the 24 Sovereign Variables to generate a slot."
    )
    parser.add_argument(
        "--show-library", action="store_true", help="Display the full, ordered character library."
    )
    args = parser.parse_args()

    if args.show_library:
        print("--- The Nonmoving Phantom (Full Character Library) ---")
        print(f"  Total Characters: {len(FULL_LIBRARY)}")
        print(f"  Sample: {''.join(FULL_LIBRARY[:75])}...")
    elif args.variable:
        braided_slot = generate_braided_slot(args.variable)
        print(f"--- Braided Cypher Slot for Variable '{args.variable}' ---")
        print(f"\n--- FRAME (Total: {len(FRAME_CHARS)}) ---")
        print(f"  Sample: {braided_slot['frame'][:20]}")
        print(f"\n--- BREATH (Total: {len(BREATH_CHARS)}) ---")
        print(f"  Sample: {braided_slot['breath']}")
    else:
        parser.print_help()
