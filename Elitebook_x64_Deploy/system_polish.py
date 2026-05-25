# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import shutil

def archive_all_test_materials():
    """
    Sweeps every test-related file into a dedicated architecture archive,
    leaving the root directory strictly for Operating System production files.
    """
    archive_dir = "lab_archives"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Patterns of files that belong in the lab archive, not the OS root
    for item in os.listdir("."):
        if item.startswith("test_") or item.endswith(".ccc") or item.endswith(".bin") or item == "__pycache__":
            # Don't archive the bridge or system cleaner
            if item in ["test_garuda_safety.py"]: # Maybe keep this one as a recent proof
                pass
            
            try:
                dest = os.path.join(archive_dir, item)
                if os.path.isdir(item):
                    shutil.move(item, dest)
                else:
                    shutil.move(item, dest)
                print(f"[CLEANER] 📦 Archived: {item}")
            except Exception as e:
                pass

    print("\n[CLEANER] 💎 Root environment polished for Gentleman Deployment.")

if __name__ == "__main__":
    archive_all_test_materials()
