# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

# codemap_viewer.py

def print_spiral(tesseract):
    current = tesseract
    while current:
        print(f"\n🌀 Generation {current.generation}")
        print(f"Traits: {current.traits}")
        print(f"Planes: {current.path['planes']}")
        print(f"Duality: {current.path['duality']}")
        current = current.child
