# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
import base64

# Define the 97-character alphabet used in the Cyclic Cypher
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
ALPHABET_LEN = len(ALPHABET)

def generate_cyclic_password(master_secret: str, site_name: str, username: str, length: int = 16) -> str:
    """
    Deterministically generates a site-specific password using the master secret and cypher alphabet.
    """
    # 1. Combine inputs to create a unique seed string for this specific site and user
    seed_string = f"{master_secret}:{site_name.lower()}:{username.lower()}"
    
    # 2. Hash the seed heavily to ensure high entropy (using SHA-256)
    hash_obj = hashlib.sha256(seed_string.encode('utf-8'))
    hash_digest = hash_obj.digest()
    
    # 3. Convert the binary hash digest into our 97-character cyclic alphabet
    password_chars = []
    
    # We use chunks of the hash digest to select characters from our alphabet
    for i in range(length):
        # Taking 2 bytes at a time and modulo by alphabet length to pick a character
        byte_index = (i * 2) % len(hash_digest)
        int_val = int.from_bytes(hash_digest[byte_index:byte_index+2], byteorder='big')
        
        # This is where the "cyclic" mapping happens
        char_index = int_val % ALPHABET_LEN
        password_chars.append(ALPHABET[char_index])
        
    generated_password = "".join(password_chars)
    return generated_password

if __name__ == "__main__":
    print("-" * 50)
    print("CYCLIC CYPHER DETERMINISTIC PASSWORD GENERATOR")
    print("-" * 50)
    
    master = input("Enter your Master Secret: ")
    site = input("Enter Website/App Name (e.g., gmail): ")
    user = input("Enter Username/Email: ")
    
    pwd = generate_cyclic_password(master, site, user, length=16)
    
    print("\n" + "=" * 50)
    print(f"Generated Password for {site}:")
    print(f">>> {pwd} <<<")
    print("=" * 50 + "\n")
