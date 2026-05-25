# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from cyberdna_engine import CyberDNAVault

def double_crunch_benchmark():
    target_file = 'lab_archives/test_iso_small.bin'
    if not os.path.exists(target_file):
        print("Target file not found.")
        return

    cdv = CyberDNAVault()
    orig_size = os.path.getsize(target_file)
    
    print("=" * 80)
    print("GARUDA V6 - DOUBLE BINARY CRUNCH BENCHMARK")
    print(f"Source: {target_file} ({orig_size:,} bytes)")
    print("=" * 80)

    # First Crunch
    crunch_1 = "crunch_layer_1.cdv6"
    print("\n[STEP 1] Executing First Crunch...")
    start_1 = time.perf_counter()
    cdv.compress(target_file, crunch_1)
    time_1 = time.perf_counter() - start_1
    size_1 = os.path.getsize(crunch_1)
    
    print(f"Crunch 1 Size: {size_1:,} bytes")
    print(f"Crunch 1 Ratio: {size_1/orig_size:.6f}")
    print(f"Crunch 1 Time: {time_1:.4f}s")

    # Second Crunch (Binary Run on the first output)
    crunch_2 = "crunch_layer_2.cdv6"
    print("\n[STEP 2] Executing Second Binary Crunch (Recursive)...")
    start_2 = time.perf_counter()
    cdv.compress(crunch_1, crunch_2)
    time_2 = time.perf_counter() - start_2
    size_2 = os.path.getsize(crunch_2)
    
    print(f"Crunch 2 (Final) Size: {size_2:,} bytes")
    print(f"Incremental Ratio: {size_2/size_1:.6f}")
    print(f"ULTIMATE TOTAL RATIO: {size_2/orig_size:.6f}")
    print(f"Crunch 2 Time: {time_2:.4f}s")

    # Verification (Round Trip check for safety)
    print("\n[STEP 3] Verifying Lossless Integrity...")
    restore_1 = "restore_1.cdv6"
    restore_orig = "restore_final.bin"
    
    cdv.decompress(crunch_2, restore_1)
    cdv.decompress(restore_1, restore_orig)
    
    with open(target_file, 'rb') as f1, open(restore_orig, 'rb') as f2:
        if f1.read() == f2.read():
            print("✅ LOSSLESS INTEGRITY VERIFIED (BIT-PERFECT RECONSTRUCTION)")
        else:
            print("❌ INTEGRITY ERROR: DATA MISMATCH DETECTED")

    # Cleanup
    for f in [crunch_1, crunch_2, restore_1, restore_orig]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    double_crunch_benchmark()
