import os
import sys
import glob
from lujan_vault import LujanVaultCLI

def get_safe_directories():
    """
    Returns a list of relatively safe directories to compress on the C: drive.
    Compressing the entire C: drive (like Windows or Program Files) WILL break the OS.
    """
    user_profile = os.environ.get("USERPROFILE", "C:")
    return [
        os.path.join(user_profile, "Downloads"),
        os.path.join(user_profile, "Documents", "OldProjects"),
        os.path.join(user_profile, "Videos", "Archives"),
        "C:\\Temp",
        "C:\\Archive"
    ]

def is_safe_file(filepath):
    """
    Check if a file is safe to compress and delete.
    Skips system files, executables, and already compressed files.
    """
    ext = filepath.lower().split('.')[-1]
    unsafe_exts = {'exe', 'dll', 'sys', 'ini', 'bat', 'cmd', 'cdv6', 'db'}
    if ext in unsafe_exts:
        return False
    
    # Avoid system folders just in case
    lower_path = filepath.lower()
    if "\\windows\\" in lower_path or "\\program files" in lower_path or "\\appdata\\" in lower_path:
        return False
        
    return True

def archive_and_delete(target_path, min_size_mb=10, dry_run=True):
    """
    Scans for unused/large files, compresses them using Lujan Deductive Vault,
    and DELETES the original to free space.
    """
    print("="*60)
    print(" 🧊 CYCLIC COMPRESSOR: C-DRIVE ARCHIVER")
    print("="*60)
    
    if dry_run:
        print("\n[!] RUNNING IN DRY-RUN MODE. No files will be modified.")
        print("[!] To actually compress and delete, run with --execute\n")
    else:
        print("\n[WARNING] RUNNING IN DESTRUCTIVE MODE.")
        print("[WARNING] Originals will be DELETED after compression.\n")

    cli = LujanVaultCLI()
    min_size_bytes = min_size_mb * 1024 * 1024
    
    # If it's a directory, walk it
    files_to_process = []
    if os.path.isdir(target_path):
        print(f"Scanning directory: {target_path}")
        for root, _, files in os.walk(target_path):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.exists(full_path) and os.path.getsize(full_path) >= min_size_bytes:
                    if is_safe_file(full_path):
                        files_to_process.append(full_path)
    elif os.path.isfile(target_path) and is_safe_file(target_path):
        files_to_process.append(target_path)

    if not files_to_process:
        print("No suitable files found to compress.")
        return

    print(f"Found {len(files_to_process)} large/unused file(s) for compression.")
    
    total_freed = 0
    for file in files_to_process:
        orig_size = os.path.getsize(file)
        print(f"\nTarget: {file} ({orig_size / (1024*1024):.2f} MB)")
        
        if not dry_run:
            try:
                # Store using double-crunch logic
                cli.store(file, deep=True, double=True)
                
                # Verify the compressed file exists before deleting original
                compressed_path = file + ".cdv6"
                if os.path.exists(compressed_path) and os.path.getsize(compressed_path) > 0:
                    os.remove(file)
                    new_size = os.path.getsize(compressed_path)
                    freed = orig_size - new_size
                    total_freed += freed
                    print(f"[DELETED] Original removed. Freed {freed / (1024*1024):.2f} MB.")
                else:
                    print(f"[ERROR] Compression failed for {file}. Original kept.")
            except Exception as e:
                print(f"[ERROR] Failed to process {file}: {e}")
        else:
            print("[DRY-RUN] Would compress and delete original.")
            
    if not dry_run:
        print("\n" + "="*60)
        print(f"ARCHIVE COMPLETE. Total Space Freed: {total_freed / (1024*1024):.2f} MB")
        print("="*60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cyclic Compressor - C-Drive Archiver")
    parser.add_argument("--path", type=str, default="SAFE_DEFAULTS", help="Specific directory to archive")
    parser.add_argument("--min-size", type=int, default=10, help="Minimum file size in MB to compress")
    parser.add_argument("--execute", action="store_true", help="Actually compress and delete originals")
    
    args = parser.parse_args()
    
    if args.path == "SAFE_DEFAULTS":
        print("No specific path provided. Will scan safe default user directories.")
        directories = get_safe_directories()
        for directory in directories:
            if os.path.exists(directory):
                archive_and_delete(directory, min_size_mb=args.min_size, dry_run=not args.execute)
    else:
        if os.path.exists(args.path):
            archive_and_delete(args.path, min_size_mb=args.min_size, dry_run=not args.execute)
        else:
            print(f"Error: Path {args.path} does not exist.")
            
    print("\n" + "-"*60)
    input("Press Enter to exit...")
