"""Debug decompression issue"""
import os

# Check what's in the compressed file
with open('test_document.ccc', 'rb') as f:
    data = f.read()
print(f'Compressed file size: {len(data)} bytes')
print(f'First 20 bytes (hex): {data[:20].hex()}')

# Check if benchmark file exists and what size it is
if os.path.exists('test_document_benchmark.txt'):
    bench_size = os.path.getsize('test_document_benchmark.txt')
    print(f'\nBenchmark output size: {bench_size} bytes')
    with open('test_document_benchmark.txt', 'rb') as f:
        sample = f.read(200)
    print(f'First 200 bytes: {sample}')
    # Get some stats
    print(f'\nFile is mostly nulls or spaces: {sample.count(b" ")} spaces, {sample.count(0)} nulls')
    os.remove('test_document_benchmark.txt')
else:
    print('No benchmark file found')
