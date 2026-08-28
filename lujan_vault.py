# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import sys
import sqlite3
import argparse
import time
from datetime import datetime
from core.cyberdna_engine import CyberDNAVault

DB_PATH = "lujan_vault.db"

class LujanVaultCLI:
    def __init__(self):
        self.engine = CyberDNAVault()
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vault_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                mode TEXT,
                original_size INTEGER,
                stored_size INTEGER,
                encoded_data BLOB,
                checksum TEXT,
                tags TEXT,
                created_at TEXT,
                recursive_mode INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def store(self, filepath, deep=False, double=False):
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found.")
            return

        filename = os.path.basename(filepath)
        original_size = os.path.getsize(filepath)
        
        output_path = filepath + ".cdv6"
        
        print(f"Initializing Deductive Scan for: {filename}")
        if deep: print("Mode: Deep Triangulation Enabled")
        if double: print("Mode: Double-Crunch Core Active (Target 90%)")
        
        if double:
            temp_path = filepath + ".cdv6.tmp"
            self.engine.compress(filepath, temp_path)
            self.engine.compress(temp_path, output_path)
            if os.path.exists(temp_path):
                os.remove(temp_path)
        else:
            self.engine.compress(filepath, output_path)
        
        stored_size = os.path.getsize(output_path)
        savings = original_size - stored_size
        ratio = (savings / original_size) * 100 if original_size > 0 else 0
        
        # Monetization logic: first 20% is gifted, everything above is monetized
        gifted_savings = min(ratio, 20.0)
        monetized_savings = max(0.0, ratio - 20.0)
        
        # Record in registry
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            INSERT INTO vault_registry 
            (filename, mode, original_size, stored_size, created_at, recursive_mode)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, "deep" if deep else "standard", original_size, stored_size, datetime.now().isoformat(), 1 if double else 0))
        conn.commit()
        conn.close()
        
        print(f"\nVault Process Complete.")
        print(f"  Result: {ratio:.2f}% Total Density Gain")
        print(f"  Randall Gift (Free): {gifted_savings:.2f}%")
        print(f"  Lujan Miracle (Premium): {monetized_savings:.2f}%")
        print(f"  Artifact: {os.path.basename(output_path)}")

    def restore(self, filepath, output_path):
        """Decompress a .cypher/.cdv6 file back to the original."""
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found.")
            sys.exit(1)
        print(f"Restoring: {os.path.basename(filepath)} -> {os.path.basename(output_path)}")
        
        current_input = filepath
        current_output = output_path
        
        self.engine.decompress(current_input, current_output)
        
        iteration = 1
        while True:
            try:
                with open(current_output, 'rb') as f:
                    magic = f.read(4)
                if magic == b'CDV6':
                    print(f"  Pass {iteration} complete. Detected dual compression layer...")
                    temp_input = current_output + ".tmp"
                    os.rename(current_output, temp_input)
                    self.engine.decompress(temp_input, current_output)
                    if os.path.exists(temp_input):
                        os.remove(temp_input)
                    iteration += 1
                else:
                    break
            except Exception as e:
                # If we can't read magic bytes, or something goes wrong, break out.
                break
                
        restored_size = os.path.getsize(output_path)
        print(f"\nVault Restore Complete.")
        print(f"  Restored: {restored_size:,} bytes -> {output_path}")

    def list_vault(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT * FROM vault_registry ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        print("\n" + "="*80)
        print("LUJAN DEDUCTIVE VAULT: RANDALL ALLOCATION AUDIT")
        print("="*80)
        print(f"{'Filename':<30} {'Orig Size':<12} {'Ratio':<10} {'Gifted':<10} {'Monetized':<10}")
        print("-"*80)
        
        total_orig = 0
        total_monetized_savings_sum = 0
        
        for row in rows:
            # Columns: id, filename, mode, original_size, stored_size, ..., created_at, recursive_mode
            filename = row[1]
            orig_size = row[3]
            stored_size = row[4]
            
            savings = orig_size - stored_size
            ratio = (savings / orig_size) * 100 if orig_size > 0 else 0
            gifted = min(ratio, 20.0)
            monetized = max(0.0, ratio - 20.0)
            
            print(f"{filename[:28]:<30} {orig_size:<12,d} {ratio:>6.2f}% {gifted:>8.2f}% {monetized:>10.2f}%")
            
            total_orig += orig_size
            total_monetized_savings_sum += (orig_size * monetized / 100)

        print("-"*80)
        print(f"TOTAL DATA OPTIMIZED: {total_orig:,} bytes")
        print(f"TOTAL REVENUE GAP:    {total_monetized_savings_sum / (1024*1024*1024) * 0.05:.2f} USD (at $0.05/GB)")
        print("="*80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lujan Deductive Vault CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Store command
    store_parser = subparsers.add_parser("store")
    store_parser.add_argument("path", help="Path to file to vault")
    store_parser.add_argument("--deep", action="store_true", help="Enable deep triangulation")
    store_parser.add_argument("--double", action="store_true", help="Enable double-crunch logic")

    # Restore command
    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("path", help="Path to .cypher file to restore")
    restore_parser.add_argument("output", help="Output path for restored file")

    # List command
    subparsers.add_parser("list")

    args = parser.parse_args()
    cli = LujanVaultCLI()

    if args.command == "store":
        cli.store(args.path, deep=args.deep, double=args.double)
    elif args.command == "restore":
        cli.restore(args.path, args.output)
    elif args.command == "list":
        cli.list_vault()
    else:
        parser.print_help()