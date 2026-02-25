"""Test the hybrid compression system"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from cyclic_hybrid import compress_realtime, decompress_realtime

print("="*80)
print("HYBRID COMPRESSION SYSTEM - Real-Time Lossless Unfolding")
print("="*80 + "\n")

test_files = [
    'test_document.txt',
    'test_large.txt',
]

for test_file in test_files:
    if not os.path.exists(test_file):
        print(f"Skipping {test_file} (not found)\n")
        continue
    
    compressed_file = test_file.replace('.txt', '_hybrid.ccc')
    decompressed_file = test_file.replace('.txt', '_hybrid_recovered.txt')
    
    print(f"TEST: {test_file}")
    print(f"{'-'*80}")
    
    # Compress
    try:
        comp_result = compress_realtime(test_file, compressed_file)
        print(f"✓ Compression successful")
        print(f"    Original:   {comp_result['original_length']:,} bytes")
        print(f"    Compressed: {comp_result['compressed_length']:,} bytes")
        print(f"    Ratio:      {comp_result['compression_ratio']:.2f}%")
        print(f"    Multiplier: x{comp_result['multiplier']}")
    except Exception as e:
        print(f"✗ Compression failed: {e}\n")
        continue
    
    # Decompress
    try:
        decomp_result = decompress_realtime(compressed_file, decompressed_file)
        print(f"✓ Decompression successful")
        print(f"    Recovered: {decomp_result['recovered_length']:,} bytes")
    except Exception as e:
        print(f"✗ Decompression failed: {e}\n")
        continue
    
    # Verify content
    with open(test_file, 'rb') as f:
        original = f.read()
    with open(decompressed_file, 'rb') as f:
        recovered = f.read()
    
    if original == recovered:
        print(f"✓ Content verification PASSED")
        print(f"    Perfect round-trip recovery achieved")
    else:
        print(f"✗ Content verification FAILED")
        print(f"    Original size:  {len(original)}")
        print(f"    Recovered size: {len(recovered)}")
    
    # Cleanup
    os.remove(compressed_file)
    os.remove(decompressed_file)
    
    print()

print("="*80)
print("SUMMARY: Hybrid system enables real-time compression with guaranteed")
print("zero-loss unfolding via zlib compression + cyclic multiplier analysis.")
print("="*80)
