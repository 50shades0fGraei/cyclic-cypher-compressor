"""Test and fix paired encoder binary format"""
import struct
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from cyclic_compressor_paired import compress_file_paired, decompress_file_paired

print("="*80)
print("PAIRED ENCODER - BINARY FORMAT VERIFICATION")
print("="*80 + "\n")

# Create fresh test files with proper encoding
test_files = [
    ('test_document.txt', 'test_document_fresh.ccc'),
    ('test_large.txt', 'test_large_fresh.ccc'),
]

print("Creating fresh compressed files with proper binary format...\n")

results = []
for input_file, output_file in test_files:
    if not os.path.exists(input_file):
        print(f"  Skipping {input_file} (not found)")
        continue
    
    # Compress
    compress_result = compress_file_paired(input_file, output_file)
    print(f"✓ {input_file}")
    print(f"    Original:   {compress_result['original_length']:,} bytes")
    print(f"    Compressed: {compress_result['compressed_length']:,} bytes")
    print(f"    Multiplier: x{compress_result['multiplier']}")
    print(f"    Ratio:      {compress_result['ratio']:.2f}%\n")
    
    # Verify binary format
    with open(output_file, 'rb') as f:
        raw_data = f.read()
    
    if len(raw_data) >= 4:
        header = struct.unpack('>I', raw_data[:4])[0]
        print(f"    Binary header check:\n")
        print(f"      Raw first 4 bytes:  {' '.join(f'{b:02x}' for b in raw_data[:4])}")
        print(f"      Interpreted as I>:  {header} (expected: {compress_result['original_length']})")
        if header == compress_result['original_length']:
            print(f"      ✓ Binary format CORRECT")
        else:
            print(f"      ✗ Binary format WRONG")
        print()
    
    # Decompress and verify
    output_restored = output_file.replace('.ccc', '_restored.txt')
    decompress_result = decompress_file_paired(output_file, output_restored)
    
    print(f"    Decompression result:")
    print(f"      Recovered:  {decompress_result['recovered_length']:,} bytes")
    print(f"      Expected:   {compress_result['original_length']:,} bytes")
    
    # Verify content
    with open(input_file, 'rb') as f:
        original = f.read()
    with open(output_restored, 'rb') as f:
        restored = f.read()
    
    if original == restored:
        print(f"      ✓ Content verification PASSED\n")
        results.append((input_file, True))
    else:
        print(f"      ✗ Content verification FAILED")
        print(f"        Original: {original[:60]}...")
        print(f"        Restored: {restored[:60]}...\n")
        results.append((input_file, False))
    
    # Cleanup
    if os.path.exists(output_restored):
        os.remove(output_restored)

print("="*80)
print("SUMMARY")
print("="*80)
for fname, passed in results:
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {fname}")
print("="*80)
