"""Test decompress_file_paired function directly"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from cyclic_compressor_paired import decompress_file_paired
    print("✓ Successfully imported decompress_file_paired")
    
    # Test decompression
    print("\nTesting decompression of test_document.ccc...")
    result = decompress_file_paired('test_document.ccc', 'test_decomp_debug.txt')
    print(f"✓ Decompression returned: {result}")
    
    if os.path.exists('test_decomp_debug.txt'):
        size = os.path.getsize('test_decomp_debug.txt')
        print(f"✓ Output file created: {size} bytes")
        os.remove('test_decomp_debug.txt')
    
except Exception as e:
    import traceback
    print(f"✗ Error: {e}")
    traceback.print_exc()
