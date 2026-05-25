# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
import os
from .syllable_codec import SyllableCodec

class VideoKeyGenerator:
    def __init__(self, master_secret):
        self.master_secret = master_secret
        self.codec = SyllableCodec()

    def generate_key(self, file_path, profile_name="default"):
        """Generates a deterministic key and pattern for a video file."""
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Combine master secret, profile name, and file metadata for uniqueness
        seed = f"{self.master_secret}:{profile_name}:{file_name}:{file_size}"
        hasher = hashlib.sha256(seed.encode('utf-8'))
        digest = hasher.digest()
        
        # 1. Generate Syllable Key (Human-Memorizable)
        ids = []
        for i in range(0, 16, 2):
            val = int.from_bytes(digest[i:i+2], 'big')
            ids.append(val % self.codec.lib_size)
        key_syllables = self.codec.decode(ids)
        
        # 2. Generate Randomized Cypher Pattern (The secret sauce)
        # We take another part of the digest to shuffle the base pattern [1,4,2,8,5,7]
        pattern_seed = digest[16:22]
        base_pattern = [1, 4, 2, 8, 5, 7]
        # Deterministic shuffle using pattern_seed
        shuffled_pattern = []
        available = list(base_pattern)
        for i in range(6):
            idx = pattern_seed[i] % len(available)
            shuffled_pattern.append(available.pop(idx))
            
        return key_syllables, digest, shuffled_pattern

if __name__ == "__main__":
    # Test (requires relative import to work, or just run as part of personal_vault.py)
    pass
