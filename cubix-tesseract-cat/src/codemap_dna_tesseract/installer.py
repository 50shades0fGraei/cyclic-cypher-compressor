# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""Installer: sets up CubixOS on the device by indexing system programs and mapping processes."""
import sys
import os
import json
from pathlib import Path
from .system_indexer import build_system_library, save_library, get_library_path, get_common_program_paths
from .spiral_pipeline import create_spiral
from .process_mapper import register_process
from .file_manager import setup_default_file_access


def setup_process_mappings(library: dict):
    """Auto-map discovered programs to function addresses."""
    print("\n🔗 Setting up process mappings...")
    
    # Group functions by program
    programs = {}
    for addr, (file_path, func_name) in library.items():
        prog = Path(file_path).parent.name.split()[0].lower()
        if prog and prog not in ("windows", "system32", "temp"):
            if prog not in programs:
                programs[prog] = []
            programs[prog].append((addr, func_name))
    
    # Register top function per program
    registered = 0
    for prog, funcs in sorted(programs.items())[:20]:  # limit to 20 programs
        if funcs:
            addr, func_name = funcs[0]
            try:
                register_process(prog, addr)
                registered += 1
            except Exception:
                pass
    
    print(f"✅ Registered {registered} process mappings")


def run_installer():
    """Interactive installer that indexes system and sets up device-specific library."""
    print("\n" + "=" * 80)
    print("🚀 CubixOS Installer")
    print("=" * 80)
    print("\nThis installer will:")
    print("  1. Scan your computer's programs")
    print("  2. Index all discoverable functions")
    print("  3. Create a device-specific function library")
    print("  4. Map processes to function addresses")
    print("  5. Set up file access ACL")
    print("  6. Save library to:", get_library_path())
    print()

    response = input("Continue? [y/n]: ").strip().lower()
    if response != "y":
        print("Installation cancelled.")
        return False

    # Scan system
    print("\n🔍 Scanning system programs...")
    scan_paths = get_common_program_paths()
    print(f"Found {len(scan_paths)} directories to scan:")
    for p in scan_paths:
        print(f"  - {p}")

    library = build_system_library(scan_paths=scan_paths, max_total=2000)
    print(f"\n✅ Indexed {len(library)} functions")

    # Save library
    lib_path = save_library(library)
    print(f"📦 Library saved to {lib_path}")

    # Setup process mappings
    setup_process_mappings(library)

    # Setup file access
    print("\n🔐 Setting up file access control...")
    setup_default_file_access()

    # Test local repo functions
    print("\n🌀 Building local function spiral...")
    try:
        spiral = create_spiral()
        print(f"✅ Local spiral created: {len(spiral.all_nodes)} functions")
    except Exception as e:
        print(f"⚠️  Local spiral failed: {e}")

    print("\n" + "=" * 80)
    print("✅ Installation complete!")
    print("=" * 80)
    print("\nYou can now use CubixOS to:")
    print("  - Call functions by address: host.py <address>")
    print("  - Route processes: python -m codemap_dna_tesseract.process_router <name>")
    print("  - Manage files: python -m codemap_dna_tesseract.file_manager [ls|read|write|delete]")
    print("  - View mappings: python -m codemap_dna_tesseract.process_mapper list")
    print("  - View file ACL: python -m codemap_dna_tesseract.file_acl list")
    print("  - Rebuild library: python -m codemap_dna_tesseract.installer --rebuild")
    print()

    return True


if __name__ == "__main__":
    rebuild = "--rebuild" in sys.argv
    if rebuild:
        print("🔄 Rebuilding system library...")
        lib = build_system_library()
        save_library(lib)
        setup_process_mappings(lib)
        print("✅ Library rebuilt and process mappings updated")
    else:
        run_installer()
