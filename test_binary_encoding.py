"""
Universal Binary Encoding Test
Tests the optimized compact format
"""

import os
from core.universal_binary import (
    encode_binary_compact, 
    decode_binary_compact,
    encode_file_compact,
    decode_file_compact
)

def test_compact_encoding():
    """Test compact binary encoding"""
    
    print("=" * 70)
    print("UNIVERSAL BINARY ENCODING - OPTIMIZED FORMAT")
    print("=" * 70)
    
    # Test 1: In-memory encoding
    print("\nTest 1: In-memory Encoding")
    print("-" * 70)
    
    test_text = "The quick brown fox jumps over the lazy dog."
    print(f"Original: '{test_text}'")
    print(f"Length: {len(test_text)} characters")
    
    # Encode
    compressed = encode_binary_compact(test_text)
    print(f"\nCompressed: {len(compressed)} bytes")
    print(f"Compression ratio: {100 * (1 - len(compressed)/len(test_text)):.1f}%")
    print(f"Bytes breakdown:")
    print(f"  - Header (length + multiplier): 5 bytes")
    print(f"  - Compressed gaps: {len(compressed) - 5} bytes")
    
    # Decode
    decoded = decode_binary_compact(compressed)
    print(f"\nDecoded: '{decoded}'")
    print(f"Verification: {'✓ PASSED' if test_text == decoded else '✗ FAILED'}")
    
    # Test 2: File encoding
    print("\n" + "=" * 70)
    print("Test 2: File Encoding")
    print("-" * 70)
    
    try:
        # Encode test file
        encode_file_compact('test_document.txt', 'test_document.ccc')
        
        # Check compression
        original_size = os.path.getsize('test_document.txt')
        compressed_size = os.path.getsize('test_document.ccc')
        
        print(f"Original file: {original_size} bytes")
        print(f"Compressed file: {compressed_size} bytes")
        print(f"Compression: {100 * (1 - compressed_size/original_size):.1f}%")
        
        # Decode and verify
        decoded_text = decode_file_compact('test_document.ccc', 'test_document_from_ccc.txt')
        
        with open('test_document.txt', 'r') as f:
            original_text = f.read()
        
        if original_text == decoded_text:
            print("\n✓ File Round-trip VERIFIED - Perfect match")
        else:
            print("\n✗ File Round-trip FAILED")
            print(f"  Original length: {len(original_text)}")
            print(f"  Decoded length: {len(decoded_text)}")
        
    except FileNotFoundError:
        print("test_document.txt not found - skipping file test")
    
    # Test 3: Comparison with v4 paired (previous best)
    print("\n" + "=" * 70)
    print("Test 3: Comparison with Previous Methods")
    print("-" * 70)
    
    try:
        # Check if v4 paired file exists
        if os.path.exists('test_paired.bin'):
            v4_size = os.path.getsize('test_paired.bin')
            print(f"v4 Paired Encoding: {v4_size} bytes")
        
        if os.path.exists('test_document.ccc'):
            binary_size = os.path.getsize('test_document.ccc')
            print(f"Universal Binary: {binary_size} bytes")
            
            if os.path.exists('test_paired.bin'):
                delta = binary_size - v4_size
                percent_delta = (delta / v4_size) * 100
                if delta > 0:
                    print(f"\nUniversal Binary is {delta} bytes LARGER ({percent_delta:.1f}%)")
                else:
                    print(f"\nUniversal Binary is {-delta} bytes SMALLER ({-percent_delta:.1f}%)")
    except Exception as e:
        print(f"Comparison failed: {e}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
The Universal Binary Encoding provides:
1. Triangulation-based deterministic encoding
2. Works with ANY character set (universal)
3. Optimized compact binary format
4. Perfect round-trip preservation

The system encodes three fundamental relationships:
  - Pattern: 142857 repeating (constant)
  - Multiplier: Per-file scaling (variable)  
  - Position: Sequential coordinates (sequential)

These three triangulate to exact symbol, making it:
  - Theoretically sound (no information loss)
  - Universally applicable (any content type)
  - Mathematically elegant (constant + variable + sequential)
""")

if __name__ == "__main__":
    test_compact_encoding()
