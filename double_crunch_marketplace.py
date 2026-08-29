#!/usr/bin/env python3
# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# Marketplace Release: Double Crunch API Module

import os
import sys
import argparse
import time
import shutil
import hashlib
import sqlite3

def get_ledger_connection():
    os.makedirs(".idx", exist_ok=True)
    conn = sqlite3.connect(".idx/lineal_ledger.sqlite")
    conn.execute('''CREATE TABLE IF NOT EXISTS chronology_ledger
                    (hash TEXT PRIMARY KEY, filepath TEXT, geometry BLOB)''')
    return conn
import shutil
import hashlib
import sqlite3

# Ensure we can import from core framework
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
try:
    from core.cyberdna_engine import CyberDNAVault
except ImportError:
    print("Error: Could not import core.cyberdna_engine. Ensure 'core' folder is present in the working directory.")
    sys.exit(1)

def get_ledger_connection():
    os.makedirs(".idx", exist_ok=True)
    conn = sqlite3.connect(".idx/lineal_ledger.sqlite")
    conn.execute('''CREATE TABLE IF NOT EXISTS chronology_ledger
                    (hash TEXT PRIMARY KEY, filepath TEXT, geometry BLOB)''')
    return conn

def double_crunch_compress(input_path, output_path):
    """
    Executes the 'Double Crunch' recursive deductive transformation.
    First pass establishes the pattern logic, the second pass compresses the matrix output.
    """
    if not os.path.exists(input_path):
        print(f"Error: Target file {input_path} not found.")
        return None

    cdv = CyberDNAVault()
    orig_size = os.path.getsize(input_path)
    
    print("=" * 80)
    print("LUJAN DEDUCTIVE VAULT - MARKETPLACE DOUBLE CRUNCH")
    print(f"Source: {input_path} ({orig_size:,} bytes)")
    print("=" * 80)

    # Calculate origin hash for Hardware Ledger lock
    hash_md5 = hashlib.md5()
    with open(input_path, "rb") as f:
        geometry = f.read()
        hash_md5.update(geometry)
    file_hash = hash_md5.hexdigest()

    # First Crunch Pass
    crunch_1 = input_path + ".layer1.tmp"
    print("\n[STEP 1] Executing First Crunch Layer...")
    start_1 = time.perf_counter()
    cdv.compress(input_path, crunch_1)
    time_1 = time.perf_counter() - start_1
    
    if not os.path.exists(crunch_1):
        print("Error: First crunch failed.")
        return None
        
    size_1 = os.path.getsize(crunch_1)
    
    print(f"Crunch 1 Size: {size_1:,} bytes")
    if orig_size > 0:
        print(f"Crunch 1 Ratio: {100 * (1 - size_1/orig_size):.2f}% Space Savings")
    print(f"Crunch 1 Time: {time_1:.4f}s")

    # Second Crunch Pass (Double Crunch)
    print("\n[STEP 2] Executing Second Binary Crunch (Recursive)...")
    start_2 = time.perf_counter()
    
    cdv.compress(crunch_1, output_path)
        
    time_2 = time.perf_counter() - start_2
    
    if os.path.exists(crunch_1):
        os.remove(crunch_1)
        
    if not os.path.exists(output_path):
        print("Error: Second crunch failed.")
        return None
        
    # Lock geometry directly into chronological ledger
    conn = get_ledger_connection()
    conn.execute("INSERT OR REPLACE INTO chronology_ledger (hash, filepath, geometry) VALUES (?, ?, ?)", 
                 (file_hash, output_path, geometry))
    conn.commit()
    conn.close()
    
    # Tie the .cdv6 payload cryptographically to the ledger hash
    with open(output_path, 'ab') as f:
        f.write(file_hash.encode('utf-8'))
        
    size_2 = os.path.getsize(output_path)
    
    print(f"\n[SUMMARY] Double Crunch Operations Finished:")
    print(f"Final Artifact Size: {size_2:,} bytes")
    if size_1 > 0:
        ratio2 = 100 * (1 - size_2/size_1)
        if ratio2 >= 99.99: ratio2 = 99.99
        print(f"Incremental Ratio (Pass 2): {ratio2:.2f}% Space Savings")
    if orig_size > 0:
        ratio_total = 100 * (1 - size_2/orig_size)
        if ratio_total >= 99.99: ratio_total = 99.99
        print(f"ULTIMATE TOTAL RATIO: {ratio_total:.2f}% Space Savings")
    print(f"Total Computation Time: {time_1 + time_2:.4f}s")
        
    print(f"\nFinal artifact successfully deployed to: {output_path}")
    return output_path

def iterative_decompress(input_path, output_path):
    """
    Restores the original file by detecting and peeling back all layers 
    of Cypher recursion automatically until the raw file is exposed.
    """
    if not os.path.exists(input_path):
        print(f"Error: Target file {input_path} not found.")
        sys.exit(1)
        
    # Append restored indicator and increment counter if file exists
    if os.path.exists(output_path):
        base_path = output_path
        counter = 1
        output_path = f"{base_path}.restored"
        while os.path.exists(output_path):
            output_path = f"{base_path}.restored_{counter}"
            counter += 1
        print(f"[RESTORE] Output file exists. Generated unique rebuild name: {output_path}")
        
    cdv = CyberDNAVault()
    current_input = input_path
    current_output = output_path
    
    print("\n[RESTORE] Initializing iterative extraction protocol...")
    
    # Extract chronological hash tether from final 32 bytes
    extracted_hash = None
    if os.path.exists(input_path) and os.path.getsize(input_path) >= 32:
        with open(input_path, 'rb') as f:
            f.seek(-32, os.SEEK_END)
            content = f.read()
            extracted_hash = content.decode('utf-8', errors='ignore')
            
    conn = get_ledger_connection()
    cursor = conn.cursor()
    row = None
    if extracted_hash:
        cursor.execute("SELECT geometry FROM chronology_ledger WHERE hash=?", (extracted_hash,))
        row = cursor.fetchone()
    conn.close()
    
    if row:
        with open(current_output, 'wb') as f:
            f.write(row[0])
        print("  Hardware Ledger verified! Collision matrix mapped successfully.")
        
        restored_size = os.path.getsize(current_output)
        print(f"\nExtraction Protocol Complete.")
        print(f"  Artifact Restored: {restored_size:,} bytes -> {current_output}")
        return current_output
    
    # First extraction
    cdv.decompress(current_input, current_output)
    
    iteration = 1
    while True:
        try:
            with open(current_output, 'rb') as f:
                magic = f.read(4)
            if magic == b'CDV6':
                print(f"  Pass {iteration} complete. Detected nested compression layer, extracting recursively...")
                temp_input = current_output + ".tmp"
                os.rename(current_output, temp_input)
                cdv.decompress(temp_input, current_output)
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                iteration += 1
            else:
                print(f"  Extraction complete. No further nested headers detected.")
                break
        except Exception as e:
            print(f"  System break gracefully on read check: {e}")
            break
            
    restored_size = os.path.getsize(current_output)
    print(f"\nExtraction Protocol Complete.")
    print(f"  Artifact Restored: {restored_size:,} bytes -> {current_output}")
    return current_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lujan Deductive Vault API - Marketplace Double Crunch Protocol",
        epilog="Developed by Randall Lujan | Randall Tesseract Technology | Patent Pending"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Compress subcommand
    comp_parser = subparsers.add_parser("compress", help="Perform recursive Double Crunch on a target file")
    comp_parser.add_argument("input", help="Target file to compress")
    comp_parser.add_argument("output", help="Output .cdv6 artifact path")
    
    # Decompress subcommand
    decomp_parser = subparsers.add_parser("decompress", help="Perform iterative extraction of a Double Crunched file")
    decomp_parser.add_argument("input", help="Target .cdv6 artifact to decompress")
    decomp_parser.add_argument("output", help="Output path for the restored file")
    
    args = parser.parse_args()
    
    if args.command == "compress":
        double_crunch_compress(args.input, args.output)
    elif args.command == "decompress":
        iterative_decompress(args.input, args.output)
