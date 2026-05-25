# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import time
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from cyberdna_engine import CyberDNAVault

def get_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk: break
            hasher.update(chunk)
    return hasher.hexdigest()

def ultimate_final_crunch_pass():
    target_file = 'lab_archives/test_iso_slice.bin'
    if not os.path.exists(target_file):
        print("Source file not found.")
        return

    cdv = CyberDNAVault()
    orig_size = os.path.getsize(target_file)
    orig_hash = get_sha256(target_file)

    print("\n" + "=" * 90)
    print(" GRAEI PROTOCOL: GARUDA V6 DEDUCTIVE VAULT - ULTIMATE FINAL PASS")
    print(" Target: Double-Binary Recursive Crunch (Null-Consolidated Architecture)")
    print("=" * 90 + "\n")

    # CRUNCH 1
    print("[PASS 1] Executing Primary Deductive Metronome Sweep...")
    crunch_1 = "ultimate_crunch_L1.cdv6"
    start_1 = time.perf_counter()
    cdv.compress(target_file, crunch_1)
    time_1 = time.perf_counter() - start_1
    size_1 = os.path.getsize(crunch_1)
    print(f"  -> CRUNCH 1 SIZE: {size_1:,} bytes ({size_1/orig_size:.6f} Ratio)")

    # CRUNCH 2
    print("\n[PASS 2] Executing Final Binary Consolidation...")
    crunch_2 = "ultimate_crunch_L2.cdv6"
    start_2 = time.perf_counter()
    cdv.compress(crunch_1, crunch_2)
    time_2 = time.perf_counter() - start_2
    size_2 = os.path.getsize(crunch_2)
    print(f"  -> CRUNCH 2 SIZE: {size_2:,} bytes")
    print(f"  -> ULTIMATE RATIO: {size_2/orig_size:.6f}")

    # UNFOLD
    print("\n[UNFOLD] Executing Recursive Molecular Reconstruction...")
    temp_restored = "ultimate_temp.cdv6"
    final_restored = "ultimate_final_restored.bin"
    
    start_unfold = time.perf_counter()
    cdv.decompress(crunch_2, temp_restored)
    cdv.decompress(temp_restored, final_restored)
    unfold_time = time.perf_counter() - start_unfold
    
    # FINAL VERIFICATION
    final_hash = get_sha256(final_restored)
    
    print("\n" + "-" * 90)
    print(f" FINAL COMPRESSION REPORT")
    print(f" Total Reduction: {100*(1-size_2/orig_size):.2f}%")
    print(f" Unfolding Speed: {os.path.getsize(final_restored)/unfold_time/1024/1024:.2f} MB/s")
    print(f" Lossless Integrity: {'BIT-PERFECT SUCCESS' if orig_hash == final_hash else 'CORRUPTION ERROR'}")
    print("-" * 90)

    if orig_hash == final_hash:
        print("\n" + "*" * 90)
        print("  MILESTONE ACHIEVED: THE GARUDA V6 WHOLE PACKAGE IS VALIDATED.")
        print("  Molecular Data Fingerprint: " + final_hash)
        print("*" * 90 + "\n")

    # Cleanup artifacts
    for f in [crunch_1, crunch_2, temp_restored, final_restored]:
        if os.path.exists(f): os.remove(f)

if __name__ == '__main__':
    ultimate_final_crunch_pass()
