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

def garuda_iso_ultimate_package():
    # Target: The 'CubixOS ISO' binary slice
    target_file = 'lab_archives/test_iso_slice.bin'
    if not os.path.exists(target_file):
        print(f"ERROR: {target_file} not found.")
        return

    cdv = CyberDNAVault()
    orig_size = os.path.getsize(target_file)
    orig_hash = get_sha256(target_file)
    
    # We will simulate a "Whole Package" by running it through the CubixOS- Paired Sequential cycle
    print("\n" + "=" * 90)
    print(" EXECUTING THE WHOLE GARUDA ISO PACKAGE")
    print(" Milestone: Recursive Binary Crunching into Vault Index")
    print("=" * 90 + "\n")

    current_input = target_file
    
    # Pass 1: Deductive Metronome Sweep
    print("[PASS 1] Executing Deductive Metronome Scan...")
    layer1 = "iso_crunch_L1.cdv6"
    cdv.compress(current_input, layer1)
    size1 = os.path.getsize(layer1)
    print(f"  -> Layer 1: {size1:,} bytes ({100*(1-size1/orig_size):.2f}% Savings)")

    # Pass 2: Paired Recursive Scan (Compressing the compressed vault)
    print("\n[PASS 2] Executing Secondary Binary Paired Crunch...")
    layer2 = "iso_crunch_L2.cdv6"
    cdv.compress(layer1, layer2)
    size2 = os.path.getsize(layer2)
    print(f"  -> Layer 2: {size2:,} bytes ({100*(1-size2/orig_size):.2f}% TOTAL Savings)")

    print("\n[STEP 3] Reconstructing CubixOS ISO Package (Total Unfold)...")
    
    # Unfold Layer 2 to Layer 1
    temp_restored = "iso_temp_restore.cdv6"
    cdv.decompress(layer2, temp_restored)
    
    # Unfold Layer 1 to Original
    final_restored = "iso_final_verified.bin"
    cdv.decompress(temp_restored, final_restored)
    
    restored_hash = get_sha256(final_restored)
    
    print("\n" + "-" * 90)
    print(f"FINAL VERIFICATION REPORT:")
    if orig_hash == restored_hash:
        print(f"  STATUS:  VERIFIED OK")
        print(f"  SIZE:    {os.path.getsize(final_restored):,} bytes (Match!)")
        print(f"  FINGERPRINT: {restored_hash[:32]}...")
    else:
        print(f"  STATUS:  CORRUPTION DETECTED")
    print("-" * 90 + "\n")

    # Final cleanup
    for f in [layer1, layer2, temp_restored, final_restored]:
        if os.path.exists(f): os.remove(f)

if __name__ == '__main__':
    garuda_iso_ultimate_package()
