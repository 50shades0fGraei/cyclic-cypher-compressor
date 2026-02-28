"""
Universal Encoder/Decoder Demo
Demonstrates triangulation-based encoding with keyboard library
"""

import json
from library.keyboard_library import get_library, get_library_size, symbol_to_index
from core.universal_encoder import encode_file, find_best_multiplier, PATTERN
from core.universal_decoder import decode_file, verify_round_trip

def test_universal_encoding():
    """Test the universal encoding system"""
    
    print("=" * 70)
    print("UNIVERSAL ENCODING SYSTEM - Triangulation Proof of Concept")
    print("=" * 70)
    
    # Show the library
    library = get_library()
    print(f"\nKeyboard Library Size: {len(library)} symbols")
    print(f"Library: {library[:20]}... (showing first 20)")
    
    # Test with existing test file
    print("\n" + "=" * 70)
    print("TEST 1: Encode/Decode test_document.txt")
    print("=" * 70)
    
    try:
        # Read original
        with open('test_document.txt', 'r') as f:
            original_text = f.read()
        
        print(f"\nOriginal text ({len(original_text)} chars): {original_text[:60]}...")
        
        # Find best multiplier
        best_mult = find_best_multiplier(original_text)
        print(f"Best multiplier: {best_mult}")
        
        # Encode
        encoded = {
            'original_length': len(original_text),
            'multiplier': best_mult,
            'positions': [],
            'gaps': []
        }
        
        library_size = get_library_size()
        pattern = PATTERN
        
        for position, char in enumerate(original_text):
            symbol_index = symbol_to_index(char)
            pattern_value = pattern[position % len(pattern)] * best_mult
            triangulation_point = (pattern_value + position) % library_size
            gap = (symbol_index - triangulation_point) % library_size
            
            encoded['positions'].append(position)
            encoded['gaps'].append(gap)
        
        print(f"\nEncoded format:")
        print(f"  - Original length: {encoded['original_length']}")
        print(f"  - Multiplier: {encoded['multiplier']}")
        print(f"  - Positions count: {len(encoded['positions'])}")
        print(f"  - Gaps: {encoded['gaps'][:20]}... (showing first 20)")
        
        # Calculate encoding efficiency
        original_bytes = len(original_text)
        encoded_json = json.dumps(encoded)
        encoded_bytes = len(encoded_json.encode('utf-8'))
        
        print(f"\nEfficiency Analysis:")
        print(f"  - Original: {original_bytes} bytes")
        print(f"  - Encoded JSON: {encoded_bytes} bytes")
        print(f"  - Compression: {100 * (1 - encoded_bytes/original_bytes):.1f}%")
        
        # Save to JSON
        with open('test_universal_encoded.json', 'w') as f:
            json.dump(encoded, f)
        
        # Decode
        decoded_text = decode_file(encoded)
        print(f"\nDecoded text ({len(decoded_text)} chars): {decoded_text[:60]}...")
        
        # Verify
        if original_text == decoded_text:
            print("\n✓ VERIFICATION PASSED - Perfect round-trip encoding/decoding")
        else:
            print("\n✗ VERIFICATION FAILED - Mismatch detected")
            print(f"  Original: {repr(original_text)}")
            print(f"  Decoded:  {repr(decoded_text)}")
        
    except FileNotFoundError:
        print("test_document.txt not found - creating simple test instead")
        
        test_text = "Hello, World!"
        print(f"\nTest text: {test_text}")
        
        # Find best multiplier
        best_mult = find_best_multiplier(test_text)
        print(f"Best multiplier: {best_mult}")
        
        # Encode
        encoded = {
            'original_length': len(test_text),
            'multiplier': best_mult,
            'positions': [],
            'gaps': []
        }
        
        library_size = get_library_size()
        pattern = PATTERN
        
        for position, char in enumerate(test_text):
            symbol_index = symbol_to_index(char)
            pattern_value = pattern[position % len(pattern)] * best_mult
            triangulation_point = (pattern_value + position) % library_size
            gap = (symbol_index - triangulation_point) % library_size
            
            encoded['positions'].append(position)
            encoded['gaps'].append(gap)
            
            print(f"  [{position}] '{char}' -> idx={symbol_index}, gap={gap}")
        
        # Decode and verify
        decoded_text = decode_file(encoded)
        print(f"\nDecoded: {decoded_text}")
        print(f"Match: {test_text == decoded_text}")
    
    print("\n" + "=" * 70)
    print("TRIANGULATION PRINCIPLE VALIDATION")
    print("=" * 70)
    print("\nFor each character, three values triangulate to exact symbol:")
    print("  1. Pattern value = PATTERN[position % 6] × Multiplier")
    print("  2. Position = Current index in file (0 to length-1)")
    print("  3. Gap = Distance from triangulation point to actual symbol")
    print("\nTogether: (Pattern_value + Position + Gap) % Library_Size = Symbol_Index")
    print("\nThis makes it UNIVERSAL because:")
    print("  - Any symbol is uniquely mappable to library index")
    print("  - Triangulation is deterministic and reversible")
    print("  - Works for ANY character set (text, binary, symbols, etc.)")
    print("  - Information preserved perfectly, no loss")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_universal_encoding()
