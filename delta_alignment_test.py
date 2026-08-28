import random
import sys

def run_alignment_test():
    print("=== STARTING DELTA ALIGNMENT VS METRONOME TEST ===\n")
    
    # 1. Setup the Parameters
    # As discussed: 3 unique cyphers, placed 6 times each = 18 total hits
    total_slots = 500  # The total length of the "time" or binary matrix
    cypher_types = ['A', 'B', 'C']
    hits_per_cypher = 6
    
    total_hits = len(cypher_types) * hits_per_cypher
    
    # 2. Generate the "Metronome" Sequence (The Raw Translation)
    # This represents the literal ticking of the computer clock (0s) with scattered cyphers
    metronome_sequence = ['0'] * total_slots
    
    # Randomly place our 18 cyphers across the 500 slots
    available_indices = list(range(total_slots))
    random.shuffle(available_indices)
    hit_indices = sorted(available_indices[:total_hits])
    
    # Assign A, B, and C to these hit points evenly
    cypher_pool = cypher_types * hits_per_cypher
    random.shuffle(cypher_pool)
    
    for idx, cypher in zip(hit_indices, cypher_pool):
        metronome_sequence[idx] = cypher
        
    metronome_string = "".join(metronome_sequence)
    
    print("1. THE METRONOME APPROACH (0s included)")
    print(f"Sample of data: {metronome_string[:80]}...")
    print(f"Total Structural Length: {len(metronome_string)} units")
    metronome_bytes = sys.getsizeof(metronome_string)
    print(f"Estimated Memory Size: {metronome_bytes} bytes\n")
    
    
    # 3. Generate the "Delta Alignment Overlay" Sequence
    # Instead of storing the 0s, we ONLY store the cypher character and the distance to it
    delta_sequence = []
    last_idx = -1
    
    for idx in hit_indices:
        delta = idx - last_idx - 1 # Distance from the last hit (or start)
        cypher = metronome_sequence[idx]
        delta_sequence.append(f"{cypher}{delta}")
        last_idx = idx
        
    delta_string = ",".join(delta_sequence)
    
    print("2. THE DELTA ALIGNMENT OVERLAY APPROACH (Gaps only)")
    print(f"Full Delta Map: {delta_string}")
    
    # We calculate the structural length based on the delta markers combined
    # e.g., 'A14' is one marker instead of 14 zeros and an A.
    delta_length = len(delta_sequence) # 18 logical markers
    print(f"Total Structural Markers: {delta_length} units (The 18 hits)")
    delta_bytes = sys.getsizeof(delta_string)
    print(f"Estimated Memory Size: {delta_bytes} bytes\n")
    
    # 4. Results & Compression Ratio
    print("3. MATHEMATICAL COMPARISON")
    print(f"Metronome Size : {metronome_bytes} bytes")
    print(f"Delta Size     : {delta_bytes} bytes")
    
    savings = 100 - ((delta_bytes / metronome_bytes) * 100)
    print(f"Size Reduction : {savings:.2f}% SPACE SAVED")
    print("\nConclusion: Recording the acoustic 'deltas' geometrically collapses the empty time (0s).")

    # 5. THE REBUILD (Decompression)
    print("\n=== THE REBUILD ===")
    
    rebuilt_sequence = []
    delta_items = delta_string.split(',')
    
    for item in delta_items:
        cypher = item[0]
        gap = int(item[1:])
        
        # Add the empty 'metronome' 0s for the elapsed gap
        rebuilt_sequence.extend(['0'] * gap)
        # Place the cypher hit
        rebuilt_sequence.append(cypher)
        
    # Pad the remaining time slots at the end (if the last cypher didn't happen exactly at slot 500)
    remaining_slots = total_slots - len(rebuilt_sequence)
    if remaining_slots > 0:
        rebuilt_sequence.extend(['0'] * remaining_slots)
        
    rebuilt_string = "".join(rebuilt_sequence)
    
    print(f"Original Stream: {metronome_string[:80]}... (Length: {len(metronome_string)})")
    print(f"Rebuilt Stream : {rebuilt_string[:80]}... (Length: {len(rebuilt_string)})")
    
    if metronome_string == rebuilt_string:
        print("\n[VERDICT: 100% BIT-PERFECT RECONSTRUCTION]")
    else:
        print("\n[ERROR: REBUILD MISMATCH]")

if __name__ == "__main__":
    run_alignment_test()
