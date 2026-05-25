# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import argparse
import hashlib
import struct
from .video_keys import VideoKeyGenerator
from .video_compressor import VideoCompressor

class PersonalVault:
    def __init__(self, master_secret):
        self.key_gen = VideoKeyGenerator(master_secret)
        self.compressor = VideoCompressor()

    def _encrypt_bytes(self, data, key_bytes):
        """Simple stream encryption for personal storage."""
        result = bytearray(len(data))
        key_len = len(key_bytes)
        for i in range(len(data)):
            result[i] = data[i] ^ key_bytes[i % key_len]
        return result

    def store(self, file_path, profile_name="default"):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return

        print(f"--- PERSONAL VAULT: SECURING VIDEO ---")
        print(f"Profile: {profile_name}")
        
        # 1. Generate Deterministic Key and Pattern
        key_name, raw_key, randomized_pattern = self.key_gen.generate_key(file_path, profile_name)
        print(f"Generated Personal Syllable Key: {key_name}")
        
        # 2. Compress the file (Deductive Metronome)
        temp_compressed = file_path + ".tmp.pvv"
        print("Compressing video using Randomized Deductive Metronome...")
        self.compressor.pattern = randomized_pattern
        self.compressor.compress(file_path, temp_compressed)
        
        # 3. Encrypt the compressed artifact
        final_output = file_path + ".pv6"
        print("Applying Personal Privacy Cypher...")
        
        # Optimized Header (15 bytes): [Magic 'PV6'][Size (4b)][Tag (8b)]
        header_magic = b'PV6'
        orig_size = os.path.getsize(file_path)
        # Use a 4-byte unsigned int for size (max 4GB, enough for personal videos usually)
        # If larger, we'd need more bytes, but let's stick to 4 for extreme efficiency.
        packed_size = struct.pack('<I', orig_size % (2**32)) 
        verification_tag = raw_key[:8]
        
        with open(temp_compressed, 'rb') as f_in, open(final_output, 'wb') as f_out:
            f_out.write(header_magic)
            f_out.write(packed_size)
            f_out.write(verification_tag)
            
            # Encrypt the entire compressed file body
            data = f_in.read()
            encrypted_body = self._encrypt_bytes(data, raw_key)
            f_out.write(encrypted_body)
            
        os.remove(temp_compressed)
        
        final_size = os.path.getsize(final_output)
        ratio = (1 - final_size / orig_size) * 100 if orig_size > 0 else 0
        
        print(f"\nVault Process Complete.")
        print(f"  Artifact: {os.path.basename(final_output)}")
        print(f"  Overhead: 15 bytes (Extreme Efficiency)")
        print(f"  Density Gain: {ratio:.2f}%")
        print(f"----------------------------------------")

    def restore(self, file_path, output_path, profile_name="default"):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return

        print(f"--- PERSONAL VAULT: RESTORING VIDEO ---")
        
        with open(file_path, 'rb') as f:
            magic = f.read(3)
            if magic != b'PV6':
                print("Error: Invalid PV6 file.")
                return
            
            packed_size = f.read(4)
            tag = f.read(8)
            orig_size_lower = struct.unpack('<I', packed_size)[0]
            
            # Since we don't store the filename, we use the output_path's name
            # as part of the key derivation. This ensures the file is "bound" to its identity.
            filename = os.path.basename(output_path)
            
            # Re-derive key
            # Note: We use the re-provided profile and the inferred filename.
            # We also use the size (we assume it fits in 4B).
            seed = f"{self.key_gen.master_secret}:{profile_name}:{filename}:{orig_size_lower}"
            body_hasher = hashlib.sha256(seed.encode('utf-8'))
            digest = body_hasher.digest()
            
            # Verify tag
            if digest[:8] != tag:
                print("Error: Key verification failed. Check Master Secret or Profile Name.")
                return
            
            print(f"Verification Successful. Restoring {filename}...")
            
            # Reconstruct the pattern correctly
            pattern_seed = digest[16:22]
            base_pattern = [1, 4, 2, 8, 5, 7]
            shuffled_pattern = []
            available = list(base_pattern)
            for i in range(6):
                idx = pattern_seed[i] % len(available)
                shuffled_pattern.append(available.pop(idx))
            
            # Decrypt body to temp pvv
            temp_pvv = file_path + ".res.tmp.pvv"
            body_data = f.read()
            decrypted_body = self._encrypt_bytes(body_data, digest)
            
            with open(temp_pvv, 'wb') as f_temp:
                f_temp.write(decrypted_body)
                
        # Decompress pvv with the randomized pattern
        self.compressor.pattern = shuffled_pattern
        self.compressor.decompress(temp_pvv, output_path)
        os.remove(temp_pvv)
        
        print(f"Restore Complete: {output_path}")
        print(f"----------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Personal Video Vault CLI (Optimized)")
    parser.add_argument("command", choices=['store', 'restore'])
    parser.add_argument("path", help="Path to file")
    parser.add_argument("--secret", required=True, help="Your Master Secret")
    parser.add_argument("--profile", default="default", help="Profile name")
    parser.add_argument("--output", help="Output path for restore")

    args = parser.parse_args()
    vault = PersonalVault(args.secret)

    if args.command == "store":
        vault.store(args.path, profile_name=args.profile)
    elif args.command == "restore":
        if not args.output:
            print("Error: --output is required for restore.")
        else:
            vault.restore(args.path, args.output, profile_name=args.profile)
