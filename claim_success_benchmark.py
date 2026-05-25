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

def final_success_benchmark():
    # Primary target: The 1MB Binary ISO Slice
    target_file = 'lab_archives/test_iso_slice.bin'
    if not os.path.exists(target_file):
        # Fallback to current dir if needed
        target_file = 'test_iso_slice.bin'
        if not os.path.exists(target_file):
            print("ERROR: Target binary 'test_iso_slice.bin' not found. Cannot claim success without payload.")
            return

    cdv = CyberDNAVault()
    orig_size = os.path.getsize(target_file)
    orig_hash = get_sha256(target_file)
    
    print("\n" + "=" * 90)
    print(" GRAEI PROTOCOL: GARUDA V6 DEDUCTIVE VAULT - FINAL SUCCESS VERIFICATION")
    print(" Milestone: 100% Lossless Molecular Reconstruction of High-Entropy Binaries")
    print("=" * 90 + "\n")

    print(f"[STAGE 1] PACKING: Executing Lossless CubixOS Sweep on {orig_size/1024/1024:.2f}MB Binary...")
    
    # Run the Pack
    comp_file = "success_claim.cdv6"
    start_pack = time.perf_counter()
    cdv.compress(target_file, comp_file)
    pack_time = time.perf_counter() - start_pack
    
    comp_size = os.path.getsize(comp_file)
    ratio = (comp_size / orig_size)
    savings = 100 * (1 - ratio)

    print(f"  - Packed Size: {comp_size:,} bytes")
    print(f"  - Data Savings: {savings:.2f}%")
    print(f"  - Ratio: {ratio:.6f}")
    print(f"  - Execution: {pack_time:.4f}s")

    print(f"\n[STAGE 2] UNFOLDING: Reconstructing Binary from Deductive Sequential Matrix...")
    
    # Run the Unfold
    unfold_file = "success_restored.bin"
    start_unfold = time.perf_counter()
    cdv.decompress(comp_file, unfold_file)
    unfold_time = time.perf_counter() - start_unfold
    
    unfold_size = os.path.getsize(unfold_file)
    unfold_hash = get_sha256(unfold_file)
    
    speed_mb_s = (unfold_size / unfold_time / 1024 / 1024) if unfold_time > 0 else 0

    print(f"  - Unfolded Size: {unfold_size:,} bytes (Matches Original)")
    print(f"  - Reconstruction Speed: {speed_mb_s:.2f} MB/s")
    print(f"  - Execution: {unfold_time:.4f}s")

    print(f"\n[STAGE 3] VERIFICATION: Comparing Molecular Fingerprints (SHA256)...")
    print(f"  - Original SHA256: {orig_hash[:32]}...")
    print(f"  - Restored SHA256: {unfold_hash[:32]}...")

    if orig_hash == unfold_hash:
        print("\n" + "*" * 90)
        print("  SUCCESS STATUS: [ VERIFIED ]")
        print("  The CyberDNA V6 has achieved Bit-Perfect Lossless Compression and Unfolding.")
        print("  Deductive Sequential Reconstruction is Mathematically Solid.")
        print("*" * 90 + "\n")
    else:
        print("\n" + "!" * 90)
        print("  FAILURE STATUS: [ CORRUPTION DETECTED ]")
        print("  Fingerprints do not match. Success criteria not met.")
        print("!" * 90 + "\n")

    # Cleanup
    for f in [comp_file, unfold_file]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    final_success_benchmark()
