# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from core.cyberdna_engine import CyberDNAVault

def unfold_partial_iso():
    input_vault = "garuda_ultimate_3gb.cdv6"
    output_restored = "garuda_iso_partial_restored.bin"
    
    if not os.path.exists(input_vault):
        print("Vault file not found.")
        return

    cdv = CyberDNAVault()
    
    print("\n" + "=" * 90)
    print(" UNFOLDING PARTIAL CYBERDNA ISO BUILD")
    print(f" Source Vault: {input_vault} ({os.path.getsize(input_vault)/1024/1024:.2f} MB)")
    print("=" * 90 + "\n")

    start = time.perf_counter()
    try:
        # Standard decompress - it should recover all completed blocks
        cdv.decompress(input_vault, output_restored)
        elapsed = time.perf_counter() - start
        
        restored_size = os.path.getsize(output_restored)
        print(f"\n[SUCCESS] Unfolding Complete.")
        print(f"  Recovered: {restored_size/1024/1024:.2f} MB")
        print(f"  Time:      {elapsed:.2f}s")
        print(f"  Speed:     {restored_size/elapsed/1024/1024:.2f} MB/s")
        
    except Exception as e:
        print(f"\n[STOPPED] Unfolding reached the termination point: {e}")
        # Check if anything was recovered before the error
        if os.path.exists(output_restored):
            print(f"  Partial recovery: {os.path.getsize(output_restored)/1024/1024:.2f} MB")

if __name__ == '__main__':
    unfold_partial_iso()
