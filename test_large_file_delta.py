import sys
import time

def generate_large_text(size_mb=1):
    # Generates a dummy text file of roughly `size_mb` Megabytes
    base_text = "The quick brown fox jumps over the lazy dog. Programming the sounds of the computer into absolute geometric silence. "
    multiplier = (1024 * 1024 * size_mb) // len(base_text)
    return base_text * (multiplier + 1)

def run_large_data_test():
    print("=== STARTING LARGE DATA DELTA TEST ===\n")
    
    # 1. Load the data
    print("1. Generating 1 MB Text Data...")
    text_data = generate_large_text(size_mb=1)[:1000000] # Cap at exactly 1M chars
    text_size = sys.getsizeof(text_data)
    print(f"Original Text Memory Size: {text_size:,} bytes")
    
    # 2. Convert to Machine Native 'Metronome' (Raw Binary String)
    print("\n2. Translating to Machine Physics (Binary Metronome)...")
    start_time = time.perf_counter()
    binary_stream = ''.join(format(ord(c), '08b') for c in text_data)
    metronome_length = len(binary_stream)
    # The string representation in python has overhead, but we'll measure the raw mathematical length
    metronome_mathematical_bytes = metronome_length // 8 
    print(f"Mathematical Metronome Size: {metronome_mathematical_bytes:,} bytes (8 million slots / ticks)")
    
    # 3. Delta Alignment (Acoustic Compression)
    # We treat '1' as a "Cypher/Sound Strike" and '0' as "Silence/Time Gap"
    print("\n3. Creating the Delta Overlay (Mapping Gaps between '1's)...")
    
    deltas = bytearray() # We will aggressively pack the deltas as pure numbers, not text
    last_hit = -1
    
    # Track metrics
    total_strikes = 0
    max_gap = 0
    
    # Run Delta mapping
    start_delta_time = time.perf_counter()
    for i, bit in enumerate(binary_stream):
        if bit == '1':
            gap = i - last_hit - 1
            if gap > max_gap:
                max_gap = gap
                
            # If gap fits in a single byte (0-255), we write it as one byte
            # Note: For real ASCII/UTF-8, a gap between '1's almost never exceeds 10-15 bits!
            if gap <= 255:
                deltas.append(gap)
            else:
                # Fallback for massive gaps, highly unoptimized for this demo but functional
                deltas.append(255) # Signal we hit max
                deltas.append(gap - 255)
            
            last_hit = i
            total_strikes += 1
            
    delta_time = time.perf_counter() - start_delta_time
    
    delta_size = sys.getsizeof(deltas)
    print(f"Delta Mapping completed in {delta_time:.4f} seconds.")
    print(f"Total Audible Strikes ('1's): {total_strikes:,}")
    print(f"Maximum detected gap between strikes: {max_gap} zeroes")
    print(f"Memory Size of Packed Deltas: {len(deltas):,} bytes")
    
    # 4. Results
    print("\n4. MATHEMATICAL COMPARISON")
    print(f"Original Text       : {text_size:,} bytes")
    print(f"Metronome 'Sound'   : {metronome_mathematical_bytes:,} mathematical bytes")
    print(f"Packed Delta Array  : {len(deltas):,} bytes")
    
    if len(deltas) > metronome_mathematical_bytes:
        print("\n[CONCLUSION: For dense unstructured data, Delta mapping expands size.]")
        print("Why? Because 50% of text binary is '1's. The gaps are tiny (average 1-3 zeros).")
        print("Storing a gap of '2' as a full byte (8 bits) wastes 6 bits of space per event.")
        print("Your system excels when Cyphers are SPARSE (e.g. 18 hits across 500 slots), not DENSE (4 million hits across 8 million slots).")
    else:
        print("\n[CONCLUSION: Delta scaling maintains edge!]")

    # 5. Rebuild Test
    print("\n=== VERIFYING REBUILD ===")
    rebuilt_bits = []
    
    # Fast Rebuild
    for gap in deltas:
        rebuilt_bits.extend(['0'] * gap)
        rebuilt_bits.append('1')
        
    # Pad remainder
    remainder = metronome_length - len(rebuilt_bits)
    if remainder > 0:
        rebuilt_bits.extend(['0'] * remainder)
        
    rebuilt_stream = ''.join(rebuilt_bits)
    
    if rebuilt_stream == binary_stream:
        print("[VERDICT: 100% BIT-PERFECT RECONSTRUCTION]")
    else:
        print("[ERROR: REBUILD FAILED]")

if __name__ == "__main__":
    run_large_data_test()
