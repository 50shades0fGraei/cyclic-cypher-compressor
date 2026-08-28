import sys
import os

current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, current_dir)
from core.cyberdna_engine import CyberDNAVault

def test():
    cdv = CyberDNAVault()
    data = b"Evaluating Randall Cryptography."
    
    print("Testing Compression...")
    packed = cdv.compress_bytes(data)
    print(f"Packed Length: {len(packed)}")
    
    # Check Magic & Seal
    print("Header bytes (expected CDV6 + RJL-ABSOLUTE):", packed[:30])
    
    print("\nTesting Authorized Decompression...")
    unpacked = cdv.decompress_bytes(packed)
    print("Unpacked Data:", unpacked.decode('utf-8'))

if __name__ == "__main__":
    test()
