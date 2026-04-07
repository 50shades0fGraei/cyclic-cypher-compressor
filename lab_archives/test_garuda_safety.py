import os
import shutil
import hashlib
from core.garuda_pack import GarudaDeductiveVault

def get_file_hash(filepath):
    """Calculate SHA-256 hash of a file for absolute verification."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def test_lossless_rebuild():
    print("==================================================")
    print(" GRAEI PROTOCOL: GARUDA V6 COMPRESSOR SAFETY TEST")
    print("==================================================")
    
    # 1. Provide a target file (We'll use a copy of our own script to test real code)
    target_file = "integrity_enforcer_core.py"
    working_copy = "integrity_test_copy.py"
    compressed_file = "integrity_test_copy.gdv6"
    restored_file = "integrity_restored.py"

    # 2. As requested: NEVER do it without copying the file first
    print(f"\n[1] Creating safe working copy of: {target_file}")
    shutil.copy2(target_file, working_copy)
    
    orig_size = os.path.getsize(working_copy)
    orig_hash = get_file_hash(working_copy)
    print(f"    - Original Size: {orig_size} bytes")
    print(f"    - Original SHA256: {orig_hash[:16]}...")
    
    # 3. Compress the Safe Copy
    print(f"\n[2] Executing Garuda V6 Deductive Compression...")
    compressor = GarudaDeductiveVault()
    compressor.compress(working_copy, compressed_file)
    
    comp_size = os.path.getsize(compressed_file)
    print(f"    - Compressed Vault Size: {comp_size} bytes")

    # 4. Rebuild from the Vault
    print(f"\n[3] Rebuilding / Decompressing from Garuda Vault...")
    compressor.decompress(compressed_file, restored_file)
    
    # 5. Verification (The crucial step)
    restored_size = os.path.getsize(restored_file)
    restored_hash = get_file_hash(restored_file)
    
    print(f"\n[4] ⚖️ MATHEMATICAL VERIFICATION")
    print(f"    - Restored Size: {restored_size} bytes")
    print(f"    - Restored SHA256: {restored_hash[:16]}...")
    
    if orig_hash == restored_hash:
        print("\n✅ VERIFICATION PASSED: The file completely rebuilt with 100% molecular accuracy.")
        print("    Data is mathematically identical to the original.")
    else:
        print("\n❌ VERIFICATION FAILED: Corruption detected in the rebuild.")

    # Clean up (Optional, leaving them so the user can inspect)
    print("\n[5] Test artifacts remaining in directory for your inspection:")
    print(f"    - {working_copy}\n    - {compressed_file}\n    - {restored_file}")

if __name__ == "__main__":
    test_lossless_rebuild()
