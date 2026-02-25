"""Inspect binary format of compressed files"""
import struct

print("Inspecting compressed file format\n")

files = [
    'test_document.ccc',
    'test_large.ccc',
]

for fname in files:
    with open(fname, 'rb') as f:
        data = f.read()
    
    print(f"{fname} ({len(data)} bytes):")
    
    # Try to read as original format
    try:
        if len(data) >= 4:
            orig_len = struct.unpack('>I', data[:4])[0]
            print(f"  First 4 bytes as big-endian uint: {orig_len}")
            if orig_len > 1000000:
                print(f"    → Suspiciously large (probably corrupt)")
            
            if len(data) > 4:
                mult = data[4]
                pairs_len = data[5] if len(data) > 5 else 0
                print(f"  Byte 5 (multiplier?): {mult}")
                print(f"  Byte 6 (pairs_len?): {pairs_len}")
                
        # Show hex dump of first 20 bytes
        print(f"  Hex dump (first 20 bytes): {' '.join(f'{b:02x}' for b in data[:20])}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()
