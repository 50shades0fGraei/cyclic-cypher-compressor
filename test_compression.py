#!/usr/bin/env python3
"""
Comprehensive test suite for the Cyclic Cypher Compressor.
Tests compression/decompression roundtrip and case preservation.
"""

import os
import json
import sys
from core.compressor import (
    load_syllable_library,
    create_letter_cyphers,
    create_syllable_cypher_map,
    compress,
    decompress
)

def test_case_preservation():
    """Test that case is preserved during compression/decompression."""
    print("\n=== Testing Case Preservation ===")
    
    # Load libraries
    syllable_library = load_syllable_library()
    vowel_map, consonant_map = create_letter_cyphers()
    c2_map = create_syllable_cypher_map(syllable_library, vowel_map, consonant_map)
    
    test_cases = [
        "The quick brown fox jumps over the lazy dog.",
        "HELLO WORLD",
        "Python Programming Language",
        "MiXeD cAsE tExT",
    ]
    
    all_passed = True
    for test_text in test_cases:
        compressed = compress(test_text, c2_map, vowel_map, consonant_map, syllable_library)
        decompressed = decompress(compressed, c2_map)
        
        if test_text == decompressed:
            print(f"✓ PASS: '{test_text}'")
        else:
            print(f"✗ FAIL: '{test_text}'")
            print(f"  Expected: {test_text}")
            print(f"  Got:      {decompressed}")
            all_passed = False
    
    return all_passed

def test_multiline_preservation():
    """Test that newlines and spaces are preserved."""
    print("\n=== Testing Multiline/Spaces Preservation ===")
    
    syllable_library = load_syllable_library()
    vowel_map, consonant_map = create_letter_cyphers()
    c2_map = create_syllable_cypher_map(syllable_library, vowel_map, consonant_map)
    
    test_text = "First line\nSecond line\nThird line"
    compressed = compress(test_text, c2_map, vowel_map, consonant_map, syllable_library)
    decompressed = decompress(compressed, c2_map)
    
    if test_text == decompressed:
        print(f"✓ PASS: Multiline text preserved")
        return True
    else:
        print(f"✗ FAIL: Multiline text not preserved")
        print(f"  Expected:\n{repr(test_text)}")
        print(f"  Got:\n{repr(decompressed)}")
        return False

def test_compression_ratio():
    """Test and display compression ratio."""
    print("\n=== Compression Ratio Test ===")
    
    syllable_library = load_syllable_library()
    vowel_map, consonant_map = create_letter_cyphers()
    c2_map = create_syllable_cypher_map(syllable_library, vowel_map, consonant_map)
    
    # Read test document
    if os.path.exists("test_document.txt"):
        with open("test_document.txt", "r") as f:
            original_text = f.read()
        
        compressed = compress(original_text, c2_map, vowel_map, consonant_map, syllable_library)
        compressed_json = json.dumps(compressed, indent=2)
        
        original_size = len(original_text.encode('utf-8'))
        compressed_size = len(compressed_json.encode('utf-8'))
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        print(f"Original size:     {original_size} bytes")
        print(f"Compressed size:   {compressed_size} bytes")
        print(f"Compression ratio: {ratio:.2f}%")
        
        return True
    else:
        print("test_document.txt not found - skipping compression ratio test")
        return True

def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Cyclic Cypher Compressor - Test Suite")
    print("=" * 50)
    
    results = [
        ("Case Preservation", test_case_preservation()),
        ("Multiline/Spaces", test_multiline_preservation()),
        ("Compression Ratio", test_compression_ratio()),
    ]
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
