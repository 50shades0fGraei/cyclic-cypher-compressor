# key/generate_syllables.py

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

def generate_syllables():
    """
    Generates a comprehensive list of syllables from Vowel/Consonant combinations.
    """
    syllables = set() # Use a set to avoid duplicates

    # CVC (e.g., "cat")
    for c1 in CONSONANTS:
        for v in VOWELS:
            for c2 in CONSONANTS:
                syllables.add(c1 + v + c2)
    
    # CV (e.g., "be")
    for c in CONSONANTS:
        for v in VOWELS:
            syllables.add(c + v)

    # VC (e.g., "at")
    for v in VOWELS:
        for c in CONSONANTS:
            syllables.add(v + c)

    # CCV (e.g., "the")
    # This is a bit more complex, we'll start with some common blends
    common_blends = ["th", "sh", "ch", "st", "sp", "sl", "tr"]
    for blend in common_blends:
        for v in VOWELS:
            syllables.add(blend + v)

    return sorted(list(syllables)) # Return as a sorted list

if __name__ == "__main__":
    syllable_list = generate_syllables()
    
    # Save the list to a file
    with open("key/syllable_library.txt", "w") as f:
        for syllable in syllable_list:
            f.write(syllable + "\n")

    print(f"Generated {len(syllable_list)} syllables and saved to key/syllable_library.txt")
