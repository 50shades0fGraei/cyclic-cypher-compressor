# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""Benchmark decompression (unfolding) performance on large datasets - Clean tracking"""
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from cyberdna_engine import CyberDNAVault
from cyclic_hybrid import compress_realtime, decompress_realtime

print("=" * 80)
print("UNFOLDING PERFORMANCE BENCHMARK - GARUDA V6 DEDUCTIVE VAULT")
print("Target: Assess '.0006' Ratio Baseline and Unfolding Speed")
print("=" * 80)

# Determine files available for robust benchmarking
test_files = []
for test_file in ['test_document.txt', 'lab_archives/test_iso_small.bin', 'lab_archives/test_iso_slice.bin']:
    if os.path.exists(test_file):
        test_files.append(test_file)

if not test_files:
    print("No test files found to benchmark. Please verify test data in directory.")
    sys.exit(1)

results = []
gdv_vault = CyberDNAVault()

for original_file in test_files:
    orig_size = os.path.getsize(original_file)
    if orig_size == 0:
        continue
    
    compressed_file = original_file + '.cdv6'
    unfolded_file = original_file + '.restored'
    
    # 1. Compress first to prepare the unfolding environment
    start_comp = time.perf_counter()
    gdv_vault.compress(original_file, compressed_file)
    comp_time = time.perf_counter() - start_comp
    comp_size = os.path.getsize(compressed_file)
    
    # 2. Benchmark Decompression (Unfolding)
    start_decomp = time.perf_counter()
    gdv_vault.decompress(compressed_file, unfolded_file)
    elapsed_decomp = time.perf_counter() - start_decomp
    
    unfolded_size = os.path.getsize(unfolded_file)
    
    # 3. Validation
    with open(original_file, 'rb') as f1, open(unfolded_file, 'rb') as f2:
        verified = (f1.read() == f2.read())
        
    ratio = comp_size / orig_size
    speed_mb_s = (unfolded_size / elapsed_decomp / (1024 * 1024)) if elapsed_decomp > 0 else 0
        
    results.append({
        'file': os.path.basename(original_file),
        'original': orig_size,
        'compressed': comp_size,
        'ratio': ratio,
        'unfolded': unfolded_size,
        'comp_time_ms': comp_time * 1000,
        'decomp_time_ms': elapsed_decomp * 1000,
        'speed_mb_s': speed_mb_s,
        'verified': verified
    })
    
    # Cleanup artifacts automatically to keep workspace pristine
    for f in [compressed_file, unfolded_file]:
        if os.path.exists(f):
             os.remove(f)

# Display Clean Results
print("\nGARUDA V6 UNFOLDING & RATIO TRACKING\n")
print(f"{'File':<25} {'Orig (B)':<10} {'Comp (B)':<10} {'Ratio':<10} {'Time (ms)':<10} {'Speed (MB/s)':<12} {'Valid':<5}")
print("-" * 85)

for r in results:
    status = "PASS" if r['verified'] else "FAIL"
    print(f"{r['file']:<25} {r['original']:<10} {r['compressed']:<10} {r['ratio']:<10.5f} {r['decomp_time_ms']:<10.2f} {r['speed_mb_s']:<12.2f} {status:<5}")

print("\n" + "=" * 80)
