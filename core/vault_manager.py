import os
import sys
# Points to your 'core' folder where engine.py and cyclic_hybrid.py live
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from cyclic_hybrid import compress_realtime, decompress_realtime

VAULT_DIR = os.path.expanduser("~/CCC_Vault")

def initialize_vault():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)
        print(f"✓ Vault initialized at {VAULT_DIR}")

def store_file(file_path):
    """Processes a regular file into a coding pair."""
    filename = os.path.basename(file_path)
    output_path = os.path.join(VAULT_DIR, filename + ".ccc")
    
    print(f"Processing {filename} into coding pairs...")
    result = compress_realtime(file_path, output_path)
    
    print(f"✓ Stored as Multiplier {result['multiplier']}")
    # Optional: os.remove(file_path) # Only if you want to replace the original
    return output_path

def retrieve_file(ccc_name, destination_path):
    """Unfolds the coding pair back into a regular file."""
    input_path = os.path.join(VAULT_DIR, ccc_name)
    decompress_realtime(input_path, destination_path)
    print(f"✓ File unfolded to {destination_path}")

if __name__ == "__main__":
    initialize_vault()
    # Example usage:
    # store_file("test_large_file.txt")
