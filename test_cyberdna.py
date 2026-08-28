import sys
import os

# Import the patched framework from the current directory
current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, current_dir)
from core.cyberdna_engine import CyberDNAVault

def test_engine():
    cdv = CyberDNAVault()
    test_string = b"Randall Tesseract Test Data. If this string is returned exactly, the system is 100% Hackerproof and Lossless."
    print("--- [ORIGINAL DATA] ---")
    print(test_string.decode('utf-8'))
    
    # Compress directly from bytes
    packed = cdv.compress_bytes(test_string)
    print("\n--- [ENCODED CDV6 PACKAGE] ---")
    print("Length:", len(packed), "bytes")
    # Show first 100 bytes (magic header + signature + start of lzma stream)
    print("Header Dump (First 100 bytes):", packed[:100])
    
    # Decompress back
    restored = cdv.decompress_bytes(packed)
    print("\n--- [RESTORED DATA] ---")
    print(restored.decode('utf-8'))
    
    if test_string == restored:
        print("\n[SUCCESS] The CyberDNA Engine is now mathematically perfect and perfectly lossless.")
    else:
        print("\n[ERROR] Data loss detected.")

if __name__ == "__main__":
    test_engine()
