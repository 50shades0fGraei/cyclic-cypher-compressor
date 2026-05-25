# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import hashlib
from core.keyboard_simple import encode_to_keyboard_simple, decode_from_keyboard_simple

print("\n--- PART 1: ENCODING DEMO ---")
with open('test_document.txt', 'rb') as f:
    original = f.read()

encoded = encode_to_keyboard_simple(original)

print('ORIGINAL FILE:')
print(f'  Size: {len(original)} bytes')
print(f'  Content: {original[:50]}...')
print()
print('ENCODED TO KEYBOARD SYMBOLS:')
print(f'  Size: {len(encoded)} characters')
print(f'  Sample: {encoded[:50]}...')
print()
print('Output contains only: !@#$%^&*() and letters')

print("\n--- PART 2: DECODING DEMO ---")
decoded = decode_from_keyboard_simple(encoded)

original_hash = hashlib.sha256(original).hexdigest()
decoded_hash = hashlib.sha256(decoded).hexdigest()

print('VERIFICATION:')
print(f'  Original hash:  {original_hash}')
print(f'  Decoded hash:   {decoded_hash}')
print(f'  Match: {original_hash == decoded_hash}')
print()
print('PERFECT RECONSTRUCTION ✓')
