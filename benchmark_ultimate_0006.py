import os
import time
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core.garuda_pack import GarudaDeductiveVault
from core.cyclic_hybrid import compress_realtime

def benchmark_garuda():
    # Looking for available binary files in lab_archives or local dir
    test_files = [
        'lab_archives/test_iso_slice.bin',   # 1MB file
        'lab_archives/test_iso_small.bin',   # 100KB file
        'test_document.txt',                 # 44 bytes text
    ]
    
    vault = GarudaDeductiveVault()
    
    print("=" * 80)
    print("GARUDA V6 DEDUCTIVE COMPRESSION vs CYCLIC COMPRESSOR")
    print("Targeting 'Ultimate .0006' Compression Benchmark")
    print("=" * 80)

    for path in test_files:
        if not os.path.exists(path):
            print(f"Skipping {path}, file not found.")
            continue
        
        orig_size = os.path.getsize(path)
        print(f"\n[FILE] {path} ({orig_size:,} bytes)")
        print("-" * 60)
        
        # Benchmark 1: Garuda Deductive
        out_g = path + '.gdv'
        start = time.perf_counter()
        vault.compress(path, out_g)
        t_g = time.perf_counter() - start
        size_g = os.path.getsize(out_g)
        ratio_g = (size_g / orig_size) if orig_size else 0
        
        print(f"  => Garuda Vault (GDV6)")
        print(f"     Compressed: {size_g:,} bytes")
        print(f"     Ratio:      {ratio_g:.6f} ({ratio_g*100:.4f}%) - Looking for 0.0006")
        print(f"     Time:       {t_g:.4f}s")
        
        # Benchmark 2: Cyclic Hybrid / Paired LZ4-style mechanism
        out_c = path + '.ccc2'
        start = time.perf_counter()
        try:
            res = compress_realtime(path, out_c)
            t_c = time.perf_counter() - start
            size_c = os.path.getsize(out_c)
            ratio_c = (size_c / orig_size) if orig_size else 0
            
            print(f"  => Cyclic Hybrid (Paired)")
            print(f"     Compressed: {size_c:,} bytes (Multiplier used: x{res['multiplier']})")
            print(f"     Ratio:      {ratio_c:.6f} ({ratio_c*100:.4f}%)")
            print(f"     Time:       {t_c:.4f}s")
        except Exception as e:
            print(f"  => Cyclic Hybrid Failed: {e}")
            
if __name__ == '__main__':
    benchmark_garuda()
