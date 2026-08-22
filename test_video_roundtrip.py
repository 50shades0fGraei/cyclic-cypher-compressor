import os, sys, hashlib, time
sys.path.insert(0, os.path.dirname(__file__))
from core.cyberdna_engine import CyberDNAVault

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

src   = 'test_video.mp4'
comp  = 'video_test.cdv6'
resto = 'video_test_restored.mp4'

vault = CyberDNAVault()

orig_size  = os.path.getsize(src)
orig_hash  = sha256(src)
print(f"\n[ORIGINAL]  {orig_size:,} bytes  SHA256: {orig_hash[:16]}...")

t0 = time.perf_counter()
vault.compress(src, comp)
t_comp = time.perf_counter() - t0
comp_size = os.path.getsize(comp)
print(f"\n[COMPRESSED] {comp_size:,} bytes  ({100*(1-comp_size/orig_size):.2f}% savings)  in {t_comp:.3f}s")

t0 = time.perf_counter()
vault.decompress(comp, resto)
t_decomp = time.perf_counter() - t0
rest_size = os.path.getsize(resto)
rest_hash = sha256(resto)
print(f"\n[RESTORED]  {rest_size:,} bytes  SHA256: {rest_hash[:16]}...")
print(f"            Decompressed in {t_decomp:.3f}s")

print(f"\n{'='*60}")
if orig_hash == rest_hash:
    print("  RESULT: ✅ BIT-PERFECT MATCH — Lossless round-trip confirmed")
else:
    print("  RESULT: ❌ HASHES DIFFER — Data was NOT faithfully reconstructed")
    print(f"  Original : {orig_hash}")
    print(f"  Restored : {rest_hash}")

# Cleanup compressed file but keep restored for inspection
os.remove(comp)
print(f"\nRestored file kept at: {resto}")
print("You can open it in a video player to inspect.")
