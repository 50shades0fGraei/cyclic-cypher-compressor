# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import json
import os

VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxz"

def generate_syllables():
    """Generates a comprehensive library of syllables."""
    syllables = set()
    
    # CVC
    for c1 in CONSONANTS:
        for v in VOWELS:
            for c2 in CONSONANTS:
                syllables.add(c1 + v + c2)
    
    # CV
    for c in CONSONANTS:
        for v in VOWELS:
            syllables.add(c + v)
            
    # VC
    for v in VOWELS:
        for c in CONSONANTS:
            syllables.add(v + c)
            
    # Blends
    blends = ["th", "sh", "ch", "st", "sp", "sl", "tr", "br", "cr", "dr", "fr", "gr", "pr", "str"]
    for blend in blends:
        for v in VOWELS:
            syllables.add(blend + v)
            
    return sorted(list(syllables), key=len, reverse=True)

class SyllableCodec:
    def __init__(self):
        self.library = generate_syllables()
        self.syllable_to_id = {s: i for i, s in enumerate(self.library)}
        self.id_to_syllable = {i: s for i, s in enumerate(self.library)}
        self.lib_size = len(self.library)

    def encode(self, text):
        """Encodes text into a list of syllable IDs."""
        ids = []
        i = 0
        while i < len(text):
            found = False
            for syllable in self.library:
                if text.lower().startswith(syllable, i):
                    ids.append(self.syllable_to_id[syllable])
                    i += len(syllable)
                    found = True
                    break
            if not found:
                # Fallback to single char if no syllable matches
                i += 1
        return ids

    def decode(self, ids):
        """Decodes syllable IDs back to text."""
        return "".join([self.id_to_syllable.get(idx, "") for idx in ids])

if __name__ == "__main__":
    codec = SyllableCodec()
    print(f"Syllable Library Size: {codec.lib_size}")
    sample = "the cat in the hat"
    encoded = codec.encode(sample)
    decoded = codec.decode(encoded)
    print(f"Sample: {sample}")
    print(f"Encoded IDs: {encoded[:10]}...")
    print(f"Decoded: {decoded}")
