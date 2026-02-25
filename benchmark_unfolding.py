"""Benchmark decompression (unfolding) performance on large datasets - Clean tracking"""
import time
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from cyclic_compressor_paired import decompress_file_paired

print("=" * 80)
print("UNFOLDING PERFORMANCE BENCHMARK - Clean Build Sequence Tracking")
print("=" * 80)

test_files = [
    ('test_document.ccc', 'test_document.txt'),
    ('test_large.ccc', 'test_large.txt'),
    ('test_final_large.ccc', 'test_final_large_restored.txt'),
]

results = []

for compressed_file, original_file in test_files:
    if not os.path.exists(compressed_file):
        continue
    
    comp_size = os.path.getsize(compressed_file)
    orig_size = os.path.getsize(original_file) if os.path.exists(original_file) else 0
    
    # Run decompression - clean, no trace output
    output_file = compressed_file.replace('.ccc', '_unfold.txt')
    start = time.perf_counter()
    info = decompress_file_paired(compressed_file, output_file)
    elapsed = time.perf_counter() - start
    
    decompressed_size = os.path.getsize(output_file)
    
    # Record essential info only
    result = {
        'file': compressed_file,
        'multiplier': info['multiplier'],
        'original': info['original_length'],
        'compressed': info['compressed_length'],
        'recovered': info['recovered_length'],
        'time_ms': elapsed * 1000
    }
    
    if decompressed_size > 0:
        result['speed_mb_s'] = decompressed_size / elapsed / 1024 / 1024
    
    # Verify correctness
    if os.path.exists(original_file):
        with open(original_file, 'rb') as f1, open(output_file, 'rb') as f2:
            original_data = f1.read()
            decompressed_data = f2.read()
            result['verified'] = original_data == decompressed_data
    
    results.append(result)
    
    # Cleanup
    if os.path.exists(output_file):
        os.remove(output_file)

# Display clean results - only build sequence and multiplier tracking
print("\nBUILD SEQUENCE & MULTIPLIER TRACKING\n")
print(f"{'File':<25} {'Multiplier':<12} {'Original':<12} {'Compressed':<12} {'Unfolded':<12} {'Time (ms)':<12} {'Status':<10}")
print("-" * 105)

for result in results:
    status = "✓" if result.get('verified', True) else "✗"
    print(f"{result['file']:<25} x{result['multiplier']:<11} {result['original']:<12} {result['compressed']:<12} {result['recovered']:<12} {result['time_ms']:<12.2f} {status:<10}")

print("\n" + "=" * 80)
