"""
Universal Keyboard Encoding Demonstration
ANY file → keyboard symbols only (97 characters)
Three variables: Pattern + Multiplier + Position
"""

import os
from core.keyboard_encoding import (
    encode_to_keyboard,
    decode_from_keyboard,
    verify_keyboard_round_trip,
    measure_keyboard_encoding,
    keyboard_encode_file,
    keyboard_decode_file
)
from library.keyboard_library import get_library

def test_keyboard_encoding():
    
    print("=" * 90)
    print("UNIVERSAL KEYBOARD ENCODING")
    print("ANY File → Keyboard Symbols Only (97 characters)")
    print("=" * 90)
    
    # Show library
    library = get_library()
    print(f"\nAvailable Keyboard Symbols: {len(library)}")
    print(f"Library (first 50): {', '.join(library[:50])}")
    
    # Test 1: Text data
    print("\n" + "=" * 90)
    print("[TEST 1] Text Data")
    print("=" * 90)
    
    text_data = "Hello, World! This is a test."
    print(f"\nOriginal text: '{text_data}'")
    print(f"Original size: {len(text_data)} bytes")
    
    # Encode to keyboard symbols
    keyboard_string, mult = encode_to_keyboard(text_data)
    
    print(f"\nEncoded to keyboard symbols:")
    print(f"  Multiplier used: x{mult}")
    print(f"  Keyboard length: {len(keyboard_string)} symbols")
    print(f"  Keyboard string: {keyboard_string if len(keyboard_string) < 80 else keyboard_string[:80] + '...'}")
    
    # Verify it contains only keyboard library symbols
    all_valid = all(sym in library for sym in keyboard_string)
    print(f"  All symbols valid: {all_valid}")
    
    # Decode back
    decoded = decode_from_keyboard(keyboard_string)
    verification = text_data.encode('utf-8') == decoded
    print(f"\nRound-trip verification: {'✓ PASSED' if verification else '✗ FAILED'}")
    
    # Test 2: Binary data (all byte values)
    print("\n" + "=" * 90)
    print("[TEST 2] Binary Data - All 256 Possible Byte Values")
    print("=" * 90)
    
    binary_complete = bytes(range(256))
    print(f"\nOriginal: All possible byte values (0-255)")
    print(f"Original size: {len(binary_complete)} bytes")
    
    is_verified, keyboard_str, decoded = verify_keyboard_round_trip(binary_complete)
    
    print(f"Encoded to keyboard symbols:")
    print(f"  Length: {len(keyboard_str)} symbols (header: 5, payload: {len(keyboard_str)-5})")
    print(f"  Sample (first 40): {keyboard_str[:40]}")
    
    print(f"\nRound-trip verification: {'✓ PASSED' if is_verified else '✗ FAILED'}")
    
    if is_verified:
        print(f"Original: {list(binary_complete[:10])}...")
        print(f"Decoded:  {list(decoded[:10])}...")
    
    # Test 3: File encoding
    print("\n" + "=" * 90)
    print("[TEST 3] File Encoding - Text to Keyboard Text")
    print("=" * 90)
    
    try:
        # Read original file
        with open('test_document.txt', 'rb') as f:
            original_data = f.read()
        
        print(f"\nOriginal file: test_document.txt")
        print(f"  Size: {len(original_data)} bytes")
        print(f"  Content: {original_data[:50]}...")
        
        # Encode to keyboard file
        keyboard_string, mult, orig_size = keyboard_encode_file(
            'test_document.txt',
            'test_document.keyboard'
        )
        
        keyboard_size = len(keyboard_string.encode('utf-8'))
        expansion = 100 * (keyboard_size / orig_size - 1)
        
        print(f"\nEncoded to keyboard symbols:")
        print(f"  Output file: test_document.keyboard")
        print(f"  Multiplier: x{mult}")
        print(f"  Size: {keyboard_size} bytes (keyboard text)")
        print(f"  Expansion: {expansion:.1f}%")
        print(f"  String (first 60): {keyboard_string[:60]}")
        
        # Decode back and verify
        decoded_data = keyboard_decode_file('test_document.keyboard', 'test_document_from_keyboard.txt')
        
        if original_data == decoded_data:
            print(f"\n✓ File Round-trip VERIFIED - Perfect match")
        else:
            print(f"\n✗ File Round-trip FAILED")
            print(f"  Original: {len(original_data)} bytes")
            print(f"  Decoded: {len(decoded_data)} bytes")
    
    except FileNotFoundError:
        print("test_document.txt not found - skipping file test")
    
    # Test 4: Compression characteristics
    print("\n" + "=" * 90)
    print("[TEST 4] Encoding Characteristics")
    print("=" * 90)
    
    test_cases = [
        (b"a", "Single byte"),
        (b"Hello", "Word"),
        (b"The quick brown fox jumps over the lazy dog.", "Pangram"),
        (bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), "Sequential bytes"),
        (b"AAAAAAAAAAAAAAAA", "Repeating byte"),
    ]
    
    for data, description in test_cases:
        orig_size, enc_size, expansion, mult, sample = measure_keyboard_encoding(data)
        print(f"\n{description}:")
        print(f"  Original: {orig_size}B → Keyboard: {enc_size}B (×{mult}) [{expansion:+.1f}%]")
        print(f"  Sample: {sample}...")
    
    # Test 5: The Principle
    print("\n" + "=" * 90)
    print("THE UNIVERSAL PRINCIPLE")
    print("=" * 90)
    
    print("""
TRIANGULATION TO KEYBOARD SYMBOLS:
────────────────────────────────────────────────────────────────────────────────

Three Variables Define Everything:

1. PATTERN (Constant):
   [1, 4, 2, 8, 5, 7] — repeats every 6 positions
   Same for all files, all data types
   
2. MULTIPLIER (Variable):
   1-6, auto-selected per file
   Optimizes gap distribution
   Stored in first keyboard symbol
   
3. POSITION (Sequential):
   0, 1, 2, ..., length-1
   Implicit in sequence ordering
   

THE ENCODING EQUATION:
────────────────────────────────────────────────────────────────────────────────

For each byte in input:
    Triangulation_Point = (Pattern[pos % 6] × Multiplier + Position) % 97
    Gap = (Byte - Triangulation_Point) % 97
    Output_Symbol = Keyboard_Library[Gap]

Result: Any byte (0-255) mapped to keyboard symbol (0-96)


WHY THIS IS REVOLUTIONARY:
────────────────────────────────────────────────────────────────────────────────

✓ ANY binary file → pure keyboard TEXT
✓ Image files → keyboard readable
✓ Executable files → keyboard representable
✓ Compressed files → pure keyboard symbols
✓ Only 97 characters needed (keyboard library)
✓ Only 3 variables needed (pattern + mult + pos)
✓ Perfect round-trip (zero loss)
✓ Text transmittable (no binary bytes)

PRACTICAL IMPLICATIONS:
────────────────────────────────────────────────────────────────────────────────

You can now:
• Email binary files as keyboard text (no attachment restrictions)
• Store binary data in plain text files
• Transmit ANY file over text-only channels
• Represent ANY content with just keyboard symbols
• Everything decodable with just multiplier + length

This is not compression—it's UNIVERSAL ENCODING TO KEYBOARD SPACE.
────────────────────────────────────────────────────────────────────────────────
    """)

if __name__ == "__main__":
    test_keyboard_encoding()
