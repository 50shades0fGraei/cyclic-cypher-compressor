import os
import tarfile
import shutil
import argparse
from double_crunch_marketplace import iterative_decompress

def unfold_legacy(archive_path="legacy_builds.cdv6", extract_path="."):
    if not os.path.exists(archive_path):
        print(f"Error: {archive_path} not found.")
        return
        
    print("==================================================")
    print("LEGACY BUILDS UNFOLDING MASTER KEY")
    print("WARNING: This restores deprecated files from the CDV6 archive.")
    print("==================================================")
    
    # Decompress the double-crunched tarball
    tarball_path = archive_path.replace(".cdv6", "_restored.tar")
    print("[1] Iteratively Unfolding CDV6 Layers...")
    iterative_decompress(archive_path, tarball_path)
    
    if os.path.exists(tarball_path):
        print(f"[2] Cypher Decompressed. Unarchiving logical structure to {os.path.abspath(extract_path)}...")
        try:
            with tarfile.open(tarball_path, "r") as tar:
                tar.extractall(path=extract_path)
            print("[SUCCESS] Legacy files have been completely restored.")
        except Exception as e:
            print(f"[ERROR] Logical structure cannot be unarchived. The Secrecy Map anchor may be missing.")
            print(f"        Engine Error: {e}")
            
        # Clean up temporary tarball
        if os.path.exists(tarball_path):
            os.remove(tarball_path)
    else:
        print("[ERROR] CDV6 unfolding failed to produce the intermediate tarball.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legacy Build Master Key (Unfold)")
    parser.add_argument("--archive", default="legacy_builds.cdv6", help="Path to the cdv6 archive")
    parser.add_argument("--outdir", default=".", help="Directory to extract to")
    args = parser.parse_args()
    
    unfold_legacy(args.archive, args.outdir)
