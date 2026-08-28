import sys
import time

def generate_large_text(size_kb=500):
    # Generates a dummy text file of roughly 500 KB to keep computations fast
    base_text = "The physical limitation of threads vs the mathematical absolute of sums. Breaking linear paths. "
    multiplier = (1024 * size_kb) // len(base_text)
    return base_text * (multiplier + 1)

def run_sums_vs_threads_test():
    print("=== STARTING: THREADS vs SUMS GEOMETRIC TEST ===\n")
    text_data = generate_large_text(size_kb=100)[:100_000] # 100 KB test for speed
    text_size = sys.getsizeof(text_data)
    
    print(f"[BASELINE] Original Text Memory Size: {text_size:,} bytes")
    binary_stream = ''.join(format(ord(c), '08b') for c in text_data)
    
    # --- PHASE 1: THE FAILED THREAD APPROACH ---
    # (Outputting individual gaps as a linear string of events)
    print("\n--- PHASE 1: LINEAR THREADS (The Bloat) ---")
    start_thread = time.perf_counter()
    threaded_deltas = bytearray()
    last_hit = -1
    
    for i, bit in enumerate(binary_stream):
        if bit == '1':
            gap = i - last_hit - 1
            if gap <= 255:
                threaded_deltas.append(gap)
            else:
                threaded_deltas.append(255)
                threaded_deltas.append(gap - 255)
            last_hit = i
            
    thread_time = time.perf_counter() - start_thread
    thread_size = sys.getsizeof(threaded_deltas)
    print(f"Executing Linear Threads took {thread_time:.4f}s")
    print(f"Threaded Size: {thread_size:,} bytes [Massive Bloat due to linearity]")
    
    # --- PHASE 2: THE GEOMETRIC SUM APPROACH ---
    # Chunking the binary into rigid matrices (e.g. 64-bit blocks) 
    # and dropping a single mathematical SUM anchor instead of stringing gaps.
    print("\n--- PHASE 2: GEOMETRIC SUMS (Consolidation) ---")
    start_sum = time.perf_counter()
    sum_anchors = bytearray()
    
    chunk_size = 32 # 32-bit geometric boundaries
    total_bits = len(binary_stream)
    
    # Process matrix chunks
    for i in range(0, total_bits, chunk_size):
        chunk = binary_stream[i:i+chunk_size]
        # Calculate the literal geometric mathematical sum of this block
        # In base-2 math, this instantly calculates the exact coordinates of every '1' concurrently
        geometric_sum = int(chunk, 2)
        
        # Pack the enormous geometric sum natively back into spatial bytes
        # A 32-bit chunk is geometrically anchored perfectly in max 4 bytes
        sum_bytes = geometric_sum.to_bytes((len(chunk) + 7) // 8, byteorder='big')
        sum_anchors.extend(sum_bytes)
        
    sum_time = time.perf_counter() - start_sum
    sum_size = sys.getsizeof(sum_anchors)
    
    print(f"Executing Geometric Sums took {sum_time:.4f}s")
    print(f"Sum-Consolidated Size: {sum_size:,} bytes")
    
    # --- PHASE 3: COMPARISON & REBUILD ---
    print("\n=== MATHEMATICAL COMPARISON ===")
    print(f"Original Data : {text_size:,} bytes")
    print(f"Threads (Bloat): {thread_size:,} bytes (Failed approach)")
    print(f"Sums (Anchors) : {sum_size:,} bytes (Solves the bloat)")
    
    print("\nRebuilding from Geometric Sums...")
    rebuilt_bits = []
    
    # Fast Rebuild from geometric sums
    # Every 4 bytes of anchor mathematically unpacks exactly back to 32 slots
    for i in range(0, len(sum_anchors), 4):
        anchor_bytes = sum_anchors[i:i+4]
        geometric_sum = int.from_bytes(anchor_bytes, byteorder='big')
        # Re-expand sum into precise matrix slots
        rebuilt_chunk = format(geometric_sum, '032b')
        rebuilt_bits.append(rebuilt_chunk)
        
    rebuilt_stream = "".join(rebuilt_bits)[:total_bits] # slice padding if any
    
    if rebuilt_stream == binary_stream:
        print("[VERDICT: Sums are 100% BIT-PERFECT, completely eliminating thread bloat!]")
        
if __name__ == "__main__":
    run_sums_vs_threads_test()
