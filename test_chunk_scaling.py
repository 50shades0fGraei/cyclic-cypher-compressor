import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from core.cyberdna_engine import CyberDNAVault

def test_large_chunk_logic():
    target_file = 'lab_archives/test_iso_slice.bin'
    if not os.path.exists(target_file):
        print("Target not found.")
        return

    orig_size = os.path.getsize(target_file)
    
    # We will test 3 different chunk sizes to see the efficiency scaling
    chunk_sizes = [
        1024 * 1024,      # 1MB
        10 * 1024 * 1024, # 10MB (Single block for this 1MB file)
        100 * 1024 * 1024 # 100MB
    ]

    print("\n" + "=" * 90)
    print(" CYBERDNA V6: CHUNK-SIZE EFFICIENCY SCALING TEST")
    print(f" Target: {target_file} ({orig_size:,} bytes)")
    print("=" * 90 + "\n")

    for size in chunk_sizes:
        print(f"[TESTING] Chunk Size: {size/1024/1024:.0f} MB")
        cdv = CyberDNAVault(chunk_size=size)
        
        output = f"chunk_test_{size}.cdv6"
        start = time.perf_counter()
        cdv.compress(target_file, output)
        elapsed = time.perf_counter() - start
        
        comp_size = os.path.getsize(output)
        ratio = comp_size / orig_size
        print(f"  -> Compressed Size: {comp_size:,} bytes")
        print(f"  -> Ratio:           {ratio:.6f} ({100*(1-ratio):.2f}% Savings)")
        print(f"  -> Time:            {elapsed:.4f}s\n")
        
        if os.path.exists(output): os.remove(output)

if __name__ == '__main__':
    test_large_chunk_logic()
