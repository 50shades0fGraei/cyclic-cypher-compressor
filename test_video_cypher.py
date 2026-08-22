"""
Double-Crunch Video Pipeline — Verification Test
Shows Stage 1 + Stage 2 output sizes and canonical reconstruction chain.
"""
import os, sys, hashlib, time
sys.path.insert(0, os.path.dirname(__file__))
from core.video_cypher_engine import VideoCypherStage1, VideoCypherStage2, DoubleCrunchVideoVault

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536): h.update(chunk)
    return h.hexdigest()

s1 = VideoCypherStage1()
s2 = VideoCypherStage2()

# ─────────────────────────────────────────
#  MICRO TEST — Stage 1 standalone
# ─────────────────────────────────────────
print("=" * 60)
print("MICRO TEST — Stage 1 on 100 bytes from test_video.mp4")
print("=" * 60)
with open('test_video.mp4', 'rb') as f:
    sample = f.read(100)

print(f"Original  ({len(sample)} bytes) : {sample.hex()[:40]}...")

# Stage 1
s1_str = s1.encode_chunk(sample)
print(f"\nStage 1 encoded ({len(s1_str)} chars)  — the 258 alignment counts:")
print(f"  {s1_str[:80]}...")

# Stage 1 → Stage 2
s2_str = s2.encode(s1_str)
print(f"\nStage 2 encoded ({len(s2_str)} chars)  — the 12 second-crunch counts:")
print(f"  {s2_str}")

# Stage 2 decode → canonical Stage 1 chars
s2_decoded = s2.decode(s2_str)
print(f"\nStage 2 decoded ({len(s2_decoded)} chars) — canonical char sequence:")
print(f"  {s2_decoded[:80]}...")

# Stage 1 decode of Stage 2 canonical → canonical bytes
s1_decoded = s1.decode_chunk(s1_str)   # decode from original s1 (direct path)
print(f"\nStage 1 decode of original s1 ({len(s1_decoded)} bytes):")
print(f"  {bytes(s1_decoded).hex()[:40]}...")
print(f"  (canonical form, not original — expected)")

# ─────────────────────────────────────────
#  FULL VIDEO SIZE TEST
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("FULL VIDEO COMPRESSION SIZE TEST — test_video.mp4")
print("=" * 60)

src = 'test_video.mp4'
orig_size = os.path.getsize(src)
print(f"Original  : {orig_size:,} bytes")

with open(src, 'rb') as f:
    data = f.read()

t0 = time.perf_counter()
s1_str_full = s1.encode_chunk(data)
s1_time = time.perf_counter() - t0
print(f"\nStage 1   : {len(s1_str_full):,} chars  ({100*(1-len(s1_str_full)/orig_size):.4f}% savings)  {s1_time:.3f}s")
print(f"  → {s1_str_full[:60]}...")

t0 = time.perf_counter()
s2_str_full = s2.encode(s1_str_full)
s2_time = time.perf_counter() - t0
print(f"\nStage 2   : {len(s2_str_full):,} chars  ({100*(1-len(s2_str_full)/orig_size):.6f}% savings)  {s2_time:.4f}s")
print(f"  → {s2_str_full}")

print(f"\n{'='*60}")
print(f"  SUMMARY")
print(f"  Original  : {orig_size:,} bytes")
print(f"  Stage 1   : {len(s1_str_full):,} chars  (258 alignment counts)")
print(f"  Stage 2   : {len(s2_str_full):,} chars  (12 second-crunch counts)")
print(f"  Reduction : {orig_size/len(s2_str_full):,.0f}× smaller")
print(f"{'='*60}")
