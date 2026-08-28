---
description: Troubleshoot Lujan Doubler Crunch Size Discrepancy for PNG files
---
Identifies and diagnoses why PNG files fail to compress with Double Crunch and traces exactly where the data expansion occurs during the systems rebuild, accounting for all files run by the engine.

// turbo-all

1. Familiarize with the project and main implementation
```bash
echo "Familiarizing with the Lujan Double Crunch implementation..."
cat core/cyberdna_engine.py | grep -E "class CyberDNAVault|def compress|def compress_bytes|lzma\.compress" 
```

2. Generate the detailed troubleshooting diagnostic script to double check the actual output
```bash
cat << 'EOF' > analyze_png_bloat.py
import os
import lzma
import sys
from core.cyberdna_engine import CyberDNAVault

def analyze_file(filepath):
    print(f"\n" + "="*80)
    print(f"--- Diagnosing Lujan Doubler Crunch Size: {filepath} ---")
    orig_size = os.path.getsize(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()
        
    print(f"Original File Size: {orig_size:,} bytes")
    
    cdv = CyberDNAVault()
    
    # 1. Simulate the precise size of the engine's internal components
    signature = cdv.encode_chunk(data[:min(len(data), 1024)])
    if len(signature) != 60:
        signature = signature.ljust(60, b'0')[:60]
    
    encoded_seal = bytes(cdv._SOVEREIGN_SEAL)
    # Accounting for Version Header if present, otherwise just Magic + Seal + Signature
    header_length = len(cdv.MAGIC) + 4 + len(encoded_seal) + 60 # +4 for "V7.1"
    
    packed = lzma.compress(data, preset=9)
    
    print(f"\n[SYSTEMS REBUILD REPORT]")
    print(f"- LZMA Output Stream Size:     {len(packed):,} bytes")
    print(f"- Aesthetic Header Overhead:   {header_length:,} bytes")
    
    total_simulated_size = header_length + len(packed)
    print(f"- Total System Rebuild Size:   {total_simulated_size:,} bytes")
    
    # 2. Run the actual program and double check the actual output artifact
    out_file = filepath + ".cdv6"
    cdv.compress(filepath, out_file)
    actual_size = os.path.getsize(out_file)
    
    print(f"\n[DOUBLE CHECK - ACTUAL ARTIFACT OUTPUT]")
    print(f"Engine processed the file to output: {out_file}")
    print(f"Actual Artifact Size on Disk:  {actual_size:,} bytes")
    
    if total_simulated_size != actual_size:
        print(f"  Warning: The simulated size ({total_simulated_size}) does not strictly match the actual physical disk size ({actual_size}). Review header versions or dictionary artifacts.")
    
    diff = actual_size - orig_size
    diff_percent = (actual_size / orig_size) * 100
    
    print(f"\n[FINAL SIZE VERDICT]")
    if actual_size > orig_size:
        print(f"❌ REBUILD BLOAT DETECTED: +{diff:,} bytes ({diff_percent:.2f}% of original)")
        print("\nDIAGNOSIS: The LZMA preset=9 algorithm failed to compress the inherently compressed PNG data. The dictionary overhead actually bloats the file above the original size. Double Crunch recursive wrappers then continue mapping metadata over this already bloated file, amplifying the size discrepancy rather than compressing.")
    else:
        print(f"✅ COMPRESSION ACHIEVED: {abs(diff):,} bytes space savings")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else 's1.png'
    if os.path.exists(target):
        analyze_file(target)
    else:
        print(f"Error: {target} not found for testing.")
EOF
```

3. Immediately run the program, check the report, and double check the actual output
```bash
python3 analyze_png_bloat.py s1.png
```

4. Validate testing on another PNG image
```bash
python3 analyze_png_bloat.py lujan_wallpaper.png
```
