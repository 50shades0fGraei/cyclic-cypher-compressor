import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from garuda_pack import GarudaDeductiveVault

def test_entropy_cap():
    target_file = 'lab_archives/test_iso_small.bin'
    
    if not os.path.exists(target_file):
        print("Missing target file.")
        return

    print("=" * 80)
    print("GARUDA V6 RECURSIVE CASCADE (ENTROPY CAP TEST)")
    print("Evaluating recursive compression limits on deductive matrices.")
    print("=" * 80)
    
    gdv = GarudaDeductiveVault()
    current_input = target_file
    orig_size = os.path.getsize(target_file)
    
    print(f"Iteration 0 (Source): {orig_size:,} bytes | Ratio: 1.000000\n")
    
    for i in range(1, 11): # Test 10 recursive layers
        current_output = f"recursive_layer_{i}.gdv6"
        
        # Compress the previous output
        gdv.compress(current_input, current_output)
        
        # Evaluate new size
        new_size = os.path.getsize(current_output)
        ratio_step = new_size / os.path.getsize(current_input) if os.path.getsize(current_input) else 0
        ratio_total = new_size / orig_size if orig_size else 0
        
        trend = "DECREASED" if new_size < os.path.getsize(current_input) else "INCREASED (ENTROPY CAP HIT)"
        
        print(f"Iteration {i}:")
        print(f"  Size:        {new_size:,} bytes")
        print(f"  Step Diff:   {ratio_step:.6f} ({trend})")
        print(f"  Total Ratio: {ratio_total:.6f} of original size\n")
        
        # Set input for next round
        current_input = current_output
        
        if trend.startswith("INCREASED"):
            print(">>> STATISTICAL CAP HAS BEEN IDENTIFIED <<<")
            break

    # Cleanup artifacts
    for i in range(1, 11):
        f = f"recursive_layer_{i}.gdv6"
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    test_entropy_cap()
