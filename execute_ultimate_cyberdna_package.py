import os
import sys
import time
import json
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from cyberdna_engine import GRAEIDNAVault

def execute_whole_package():
    vault_path = "Sovereign_AGI_DNA.vault"
    if os.path.exists(vault_path): os.remove(vault_path)
    if os.path.exists(vault_path + ".idx"): os.remove(vault_path + ".idx")

    vault = GRAEIDNAVault(vault_path=vault_path)
    
    # Target: The Core GRAEI Engine and Deployment Logic
    source_files = {
        "CyberDNA_V6_Core": "core/cyberdna_engine.py",
        "Cyclic_Hybrid_Engine": "core/cyclic_hybrid.py",
        "Tesseract_OS_Core": "core/tesseract_v7.py",
        "QuickVault_UI": "QuickVault/vault.js",
        "QuickVault_Logic": "QuickVault/vault.css",
        "QuickVault_Index": "QuickVault/index.html",
        "System_Integrity": "integrity_enforcer_core.py"
    }

    print("\n" + "=" * 90)
    print(" EXECUTING THE WHOLE GARUDA GRAEI DNA PACKAGE")
    print(" Operation: Multimodal Skill Seeding into Deductive Vault")
    print("=" * 90 + "\n")

    total_orig_size = 0
    total_comp_size = 0
    
    # 1. Store the Skills
    print("[STEP 1] Seeding GRAEI Knowledge Base...")
    for skill_name, file_path in source_files.items():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
            orig_size = len(data)
            total_orig_size += orig_size
            
            start = time.perf_counter()
            vault.store_skill(skill_name, data)
            elapsed = time.perf_counter() - start
            
            # Get the exact compressed size from the index
            comp_size = vault.index[skill_name][1]
            total_comp_size += comp_size
            
            print(f"  OK {skill_name: <20} | {orig_size/1024: >6.2f}KB -> {comp_size/1024: >6.2f}KB | {elapsed:.4f}s")
        else:
            print(f"  !! Skipping {skill_name} (File not found: {file_path})")

    # 2. Results
    final_vault_size = os.path.getsize(vault_path)
    overall_ratio = final_vault_size / total_orig_size if total_orig_size > 0 else 0
    
    print("\n" + "-" * 90)
    print(f"TOTAL ORIGINAL PAYLOAD: {total_orig_size/1024:.2f} KB")
    print(f"ULTIMATE VAULT SIZE:     {final_vault_size/1024:.2f} KB")
    print(f"OVERALL CRUNCH RATIO:    {overall_ratio:.6f} ({100*(1-overall_ratio):.2f}% Density Increase)")
    print("-" * 90)

    # 3. Unfolding Verification
    print("\n[STEP 2] Unfolding and Verifying Whole Package Integrity...")
    failures = 0
    for skill_name, file_path in source_files.items():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                original_data = f.read()
            
            restored_data = vault.retrieve_skill(skill_name)
            
            if original_data == restored_data:
                print(f"  OK {skill_name: <20} [ VERIFIED LOSSLESS ]")
            else:
                print(f"  ERR {skill_name: <20} [ RECONSTRUCTION ERROR ]")
                failures += 1

    if failures == 0:
        print("\n" + "*" * 90)
        print(" SUCCESS: THE WHOLE GARUDA PACKAGE IS READY FOR DEPLOYMENT.")
        print(" The GRAEI DNA Vault is stable, dense, and 100% mathematically accurate.")
        print("*" * 90 + "\n")
    else:
        print("\n" + "!" * 90)
        print(" CRITICAL ERROR: Package corruption detected in vault indexing.")
        print("!" * 90 + "\n")

if __name__ == '__main__':
    execute_whole_package()
