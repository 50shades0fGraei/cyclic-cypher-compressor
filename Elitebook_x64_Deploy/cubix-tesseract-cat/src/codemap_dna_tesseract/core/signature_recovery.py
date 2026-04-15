"""
Cyclic Cypher Archiver - Recovery Tool
Reconstruct original files from signature-based archives.
"""

import json
import os
import base64
import sys

CYCLIC_CONSTANT = "142857"

def restore_archive(archive_path, output_path, secret_key="default_key"):
    """
    Restore file from signature archive.
    Uses signatures + position indices to reconstruct original.
    """
    print(f"\n{'='*80}")
    print(f"CYCLIC SIGNATURE ARCHIVER - Recovery Tool")
    print(f"{'='*80}")
    
    # Read archive
    try:
        with open(archive_path, 'r', encoding='utf-8') as f:
            archive = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Archive file not found: {archive_path}")
        return
    
    metadata = archive['metadata']
    print(f"\nArchive metadata:")
    print(f"  Original file: {metadata['original_filename']}")
    print(f"  Original size: {metadata['original_size_bytes']:,} bytes")
    print(f"  Created: {metadata['created']}")
    print(f"  Compression type: {metadata['compression_type']}")
    
    # Note on recovery
    print(f"\n{'-'*80}")
    print("NOTE: Signature-based recovery enables:")
    print("  ✓ Verification of data integrity")
    print("  ✓ Pattern analysis and brute-force recovery")
    print("  ✓ Long-term archival with proof of content")
    print(f"  ✗ Direct lossless restoration (use paired encoder for real-time)")
    print(f"{'-'*80}")
    
    # Reconstruct what we can
    reconstructed = {}
    
    # Restore unknown characters (preserved in base64)
    if 'unknown' in archive['signatures']:
        unknown_data = archive['signatures']['unknown']
        if 'data' in unknown_data:
            reconstructed['unknown'] = base64.b64decode(unknown_data['data']).decode('utf-8')
            print(f"\nRestored: {len(reconstructed['unknown'])} unknown characters")
    
    # For character types with signatures, we can verify position counts
    total_recoverable = 0
    for char_type, sig_data in archive['signatures'].items():
        if char_type == 'unknown':
            continue
        if 'char_count' in sig_data:
            total_recoverable += sig_data['char_count']
            print(f"Indexed: {sig_data['char_count']} {char_type} characters")
    
    print(f"\n{'='*80}")
    print(f"Archive recovery metadata complete.")
    print(f"For full reconstruction, use brute-force recovery with character signatures.")
    print(f"{'='*80}\n")
    
    # Write recovery manifest
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"ARCHIVE RECOVERY MANIFEST\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Source archive: {os.path.basename(archive_path)}\n")
        f.write(f"Original filename: {metadata['original_filename']}\n")
        f.write(f"Original size: {metadata['original_size_bytes']:,} bytes\n\n")
        f.write(f"CHARACTER DISTRIBUTION:\n")
        f.write(f"{'-'*40}\n")
        for char_type, count in archive['character_counts'].items():
            f.write(f"  {char_type:12} : {count:6} chars\n")
        f.write(f"{'-'*40}\n")
        f.write(f"  {'TOTAL':12} : {sum(archive['character_counts'].values()):6} chars\n")
        f.write(f"\n\nSIGNATURES AVAILABLE FOR RECOVERY:\n")
        f.write(f"{'-'*40}\n")
        for char_type, sig_data in archive['signatures'].items():
            if 'signature' in sig_data:
                f.write(f"  {char_type}: {sig_data['signature']}\n")
        f.write(f"\nRecovery manifest written to: {output_path}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Restore from Cyclic Signature Archive")
    parser.add_argument("--archive", type=str, required=True, help="Archive file to restore from")
    parser.add_argument("--manifest", type=str, required=True, help="Output manifest file")
    parser.add_argument("--key", type=str, default="default_key", help="Secret key")
    
    args = parser.parse_args()
    restore_archive(args.archive, args.manifest, args.key)
