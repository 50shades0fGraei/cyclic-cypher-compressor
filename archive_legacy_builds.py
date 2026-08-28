import os
import tarfile
import shutil
from double_crunch_marketplace import double_crunch_compress

def archive_legacy(folders_to_archive, archive_name="legacy_builds.cdv6"):
    print("==================================================")
    print("LEGACY ARCHIVER: PACKAGING AND COMPRESSING DEPRECATED BUILDS")
    print("==================================================")
    
    tarball = "legacy_staging.tar"
    print(f"[1] Tarballing target directories into {tarball}...")
    
    with tarfile.open(tarball, "w") as tar:
        for folder in folders_to_archive:
            if os.path.exists(folder):
                print(f"  -> Archiving {folder}...")
                tar.add(folder, arcname=os.path.basename(folder))
            else:
                print(f"  -> Skipping {folder} (Not found)")
    
    if not os.path.exists(tarball) or os.path.getsize(tarball) == 0:
        print("Error: Tarball creation failed or was empty.")
        return

    print(f"\n[2] Executing CDV6 Engine Double Crunch on {tarball}...")
    result_path = double_crunch_compress(tarball, archive_name)
    
    if result_path and os.path.exists(result_path):
        print(f"\n[3] PROTOCOL CHECK: Verifying Artifact Integrity Before Purge...")
        
        # We must decompress it to verify structural integrity
        test_decompress_path = "legacy_staging_test_verify.tar"
        
        from core.cyberdna_engine import CyberDNAVault
        cdv = CyberDNAVault()
        cdv.decompress(result_path, test_decompress_path)
        
        import hashlib
        def hash_file(path):
            if not os.path.exists(path): return None
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            return h.hexdigest()
            
        hash_orig = hash_file(tarball)
        hash_test = hash_file(test_decompress_path)
        
        if hash_orig and hash_test and hash_orig == hash_test:
            print("[✓] Integrity verified. Decompressed artifact matches original tarball SHA-256.")
            print(f"\n[4] Purging original folders to absolute cypher abstraction...")
            for folder in folders_to_archive:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                    print(f"  -> Purged {folder}")
            
            # Remove tarball structures
            if os.path.exists(tarball): os.remove(tarball)
            if os.path.exists(test_decompress_path): os.remove(test_decompress_path)
                
            print(f"\n[SUCCESS] Legacy files are successfully archived and removed.")
            print(f"  Encrypted Archive: {archive_name}")
            print(f"  Master Key: legacy_unfold_key.py")
        else:
            print("[CRITICAL ERROR] Integrity check failed. Checksums do not match.")
            print(f"Original: {hash_orig}")
            print(f"Restored: {hash_test}")
            print("[ACTION REQUIRED] Deletion aborted. The source files have been preserved.")
    else:
        print("[ERROR] Failed to double crunch the archive.")

if __name__ == "__main__":
    TARGETS = [
        "QuickVault",
        "dist_archiver",
        "Elitebook_x64_Deploy",
        "cubix-os-prototype"
    ]
    archive_legacy(TARGETS)
