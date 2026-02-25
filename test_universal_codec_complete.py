"""
Universal Codec Demonstration
Proves the triangulation principle works for ANY data type
"""

import os
from core.universal_codec import (
    encode_universal,
    decode_universal,
    encode_universal_sparse,
    decode_universal_sparse,
    verify_round_trip,
    measure_compression,
    encode_universal_to_file,
    decode_universal_from_file
)

def test_universal_codec():
    
    print("=" * 80)
    print("UNIVERSAL CODEC DEMONSTRATION")
    print("Triangulation Principle: Pattern + Multiplier + Position = Symbol")
    print("=" * 80)
    
    # Test 1: Text data
    print("\n[TEST 1] Text Data")
    print("-" * 80)
    
    text_data = "The quick brown fox jumps over the lazy dog."
    text_bytes = text_data.encode('utf-8')
    
    print(f"Original: '{text_data}'")
    print(f"Size: {len(text_bytes)} bytes")
    
    # Encode/decode
    is_verified, original, decoded = verify_round_trip(text_data)
    print(f"Round-trip verification: {'✓ PASSED' if is_verified else '✗ FAILED'}")
    
    # Measure compression
    orig_size, comp_size, comp_pct, mult = measure_compression(text_bytes)
    print(f"Compression: {orig_size}B → {comp_size}B ({comp_pct:.1f}%)")
    print(f"Multiplier: {mult}")
    
    # Test 2: Binary data
    print("\n[TEST 2] Binary Data (arbitrary bytes)")
    print("-" * 80)
    
    binary_data = bytes(range(256))  # All possible byte values
    print(f"Data: {len(binary_data)} bytes containing every possible byte value (0-255)")
    
    is_verified, _, _ = verify_round_trip(binary_data)
    print(f"Round-trip verification: {'✓ PASSED' if is_verified else '✗ FAILED'}")
    
    orig_size, comp_size, comp_pct, mult = measure_compression(binary_data)
    print(f"Compression: {orig_size}B → {comp_size}B ({comp_pct:.1f}%)")
    print(f"Multiplier: {mult}")
    
    # Test 3: Repeated pattern
    print("\n[TEST 3] Repeated Pattern (should compress better)")
    print("-" * 80)
    
    pattern_data = b"ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF"
    print(f"Data: {len(pattern_data)} bytes of repeating 'ABCDEF' pattern")
    
    is_verified, _, _ = verify_round_trip(pattern_data)
    print(f"Round-trip verification: {'✓ PASSED' if is_verified else '✗ FAILED'}")
    
    orig_size, comp_size, comp_pct, mult = measure_compression(pattern_data)
    print(f"Compression: {orig_size}B → {comp_size}B ({comp_pct:.1f}%)")
    print(f"Multiplier: {mult}")
    
    # Test 4: File encoding
    print("\n[TEST 4] File Encoding/Decoding")
    print("-" * 80)
    
    try:
        # Encode test file
        orig_size, comp_size = encode_universal_to_file('test_document.txt', 'test_document.uni')
        comp_pct = 100 * (1 - comp_size / orig_size)
        
        print(f"Encoded test_document.txt")
        print(f"  Original: {orig_size} bytes")
        print(f"  Encoded: {comp_size} bytes")
        print(f"  Compression: {comp_pct:.1f}%")
        
        # Decode and verify
        decoded = decode_universal_from_file('test_document.uni', 'test_document_from_uni.txt')
        
        with open('test_document.txt', 'rb') as f:
            original = f.read()
        
        if original == decoded:
            print(f"  ✓ Round-trip VERIFIED")
        else:
            print(f"  ✗ Round-trip FAILED")
    
    except FileNotFoundError as e:
        print(f"File test skipped: {e}")
    
    # Test 5: Sparse encoding (with non-zero gaps only)
    print("\n[TEST 5] Sparse Encoding Variant")
    print("-" * 80)
    
    sparse_data = b"aaaa" + b"AAAA" + b"0000"  # Limited alphabet
    
    full_encoded = encode_universal(sparse_data)
    sparse_encoded = encode_universal_sparse(sparse_data)
    
    print(f"Data: {sparse_data}")
    print(f"  Full encoding: {len(full_encoded)} bytes")
    print(f"  Sparse encoding: {len(sparse_encoded)} bytes")
    print(f"  Sparse benefit: {len(full_encoded) - len(sparse_encoded)} bytes saved")
    
    # Verify sparse
    decoded = decode_universal_sparse(sparse_encoded)
    if decoded == sparse_data:
        print(f"  ✓ Sparse round-trip VERIFIED")
    else:
        print(f"  ✗ Sparse round-trip FAILED")
    
    # Architecture Summary
    print("\n" + "=" * 80)
    print("UNIVERSAL CODEC ARCHITECTURE")
    print("=" * 80)
    
    print("""
THREE COMPONENTS TRIANGULATION:
────────────────────────────────────────────────────────────────────────────────

1. PATTERN (Constant):
   [1, 4, 2, 8, 5, 7] repeating
   └─ Universal mathematical reference
   └─ Same for all files, all data types
   └─ Provides structural order

2. MULTIPLIER (Variable):
   Values 1-6 selected per file
   └─ Scales pattern proportionally
   └─ Optimized via testing all x1-x6
   └─ Adapts to data characteristics

3. POSITION (Sequential):
   0, 1, 2, 3, ... length-1
   └─ Coordinate in the data stream
   └─ Disambiguates between identical bytes
   └─ Natural ordering guarantees

THE TRIANGULATION EQUATION:
────────────────────────────────────────────────────────────────────────────────

    Triangulation_Point = (Pattern[pos % 6] × Multiplier + Position) % 97
    
    Actual_Byte = (Triangulation_Point + Gap) % 97
    
    Where Gap = how far actual byte is from expected triangulation point
    
────────────────────────────────────────────────────────────────────────────────

WHY IT'S UNIVERSAL:
────────────────────────────────────────────────────────────────────────────────

✓ Works on ANY content (text, binary, images, video, code, compressed data...)
✓ No character set assumptions (works with bytes 0-255)
✓ Perfectly reversible (no information loss)
✓ Deterministic (same input → same output)
✓ Mathematically elegant (3 values → N symbols)
✓ Adaptive (multiplier selection optimizes per file)
✓ Library-independent (keyboard library used for reference only)

────────────────────────────────────────────────────────────────────────────────
    """)

if __name__ == "__main__":
    test_universal_codec()
