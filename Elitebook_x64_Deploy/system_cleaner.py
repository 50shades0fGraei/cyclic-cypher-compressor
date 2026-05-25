# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import shutil
import time

def organize_sovereign_workspace():
    """
    Cleans up the workspace from test artifacts and ensures 
    a 'Gentlemanly' professionalism for the Sovereign OS.
    """
    print("\n[SYSTEM CLEANSER] 🧹 Initiating Workspace Optimization...")
    
    # Files to clear from the root as they were just test artifacts
    junk_list = [
        "integrity_test_copy.py",
        "integrity_test_copy.cdv6",
        "integrity_restored.py",
        "healthcare_audit.log"
    ]
    
    # Create directories if they don't exist for better structure
    dirs = ["vault", "logs", "graei_dna"]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"[SYSTEM] Created Directory: ./{d}/")

    # Move/Delete junk
    for junk in junk_list:
        if os.path.exists(junk):
            os.remove(junk)
            print(f"[SYSTEM] 🗑️ Erased Junk: {junk}")

    # Move bridge/security logs to formal logs directory if they exist
    if os.path.exists("graei_dna.vault"):
        shutil.move("graei_dna.vault", "graei_dna/sovereign.vault")
        if os.path.exists("graei_dna.vault.idx"):
            shutil.move("graei_dna.vault.idx", "graei_dna/sovereign.vault.idx")
        print("[SYSTEM] 🧬 Migrated GRAEI DNA Vault into protected sub-directory.")

    print("[SYSTEM CLEANSER] ✅ Workplace Cleanliness: 100%. Protocol: Gentleman First.\n")

if __name__ == "__main__":
    organize_sovereign_workspace()
