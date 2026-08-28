import math
import random
import time

def calculate_packed_size(int_array):
    """
    Calculates the exact theoretical byte size if we packed the array
    using only the exact number of bits required for the maximum absolute value.
    This simulates stripping away all unused 0s in the hardware mapping.
    """
    if not int_array: return 0
    max_val = max(abs(x) for x in int_array)
    if max_val == 0:
        required_bits_per_num = 1
    else:
        # +1 for the sign bit (positive/negative displacement)
        required_bits_per_num = math.ceil(math.log2(max_val + 1)) + 1
        
    total_bits = len(int_array) * required_bits_per_num
    return math.ceil(total_bits / 8) # Convert to bytes

def deductive_pass(input_array):
    """
    Runs one pass of Deductive Displacement.
    Takes an array of sums, outputs the derivative (difference) array.
    """
    if len(input_array) <= 1: return input_array
    
    displacements = [input_array[0]] # Keep the first anchor
    for i in range(1, len(input_array)):
        displacements.append(input_array[i] - input_array[i-1])
        
    return displacements

def run_recursive_test(name, data_bytes):
    print(f"\n==========================================")
    print(f" TESTING: {name.upper()}")
    print(f"==========================================")
    
    original_size = len(data_bytes)
    print(f"Original Size: {original_size:,} bytes")
    
    # Pass 0: Convert bytes to integers
    current_array = list(data_bytes)
    current_size = original_size
    
    passes = 0
    max_passes = 1000 # Safety limit
    
    # Target is 99% compression (meaning size <= 1% of original)
    target_size = math.ceil(original_size * 0.01)
    
    print(f"Targeting 99% Compression ({target_size:,} bytes)...")
    
    while passes < max_passes:
        passes += 1
        # Run the pass
        next_array = deductive_pass(current_array)
        next_size = calculate_packed_size(next_array)
        
        compression_ratio = 100 - ((next_size / original_size) * 100)
        
        # Check diminishing returns / Entropy Wall
        if next_size >= current_size and passes > 2:
            print(f"--> [DIMINISHING RETURN HIT] at Pass {passes}")
            print(f"--> Cycle size bounced/stalled: {next_size:,} bytes vs {current_size:,} bytes")
            print(f"--> Max Compression Achieved: {100 - ((current_size / original_size) * 100):.2f}%")
            break
            
        current_array = next_array
        current_size = next_size
        
        if current_size <= target_size:
            print(f"--> [99% TARGET ACHIEVED] at Pass {passes}!")
            print(f"--> Final Size: {current_size:,} bytes")
            break
            
        # Logging every 50 passes to avoid terminal spam
        if passes % 50 == 0:
            print(f"Pass {passes:3d} | Size: {current_size:,} bytes | {compression_ratio:.2f}% Compressed")

def main():
    print("=== MULTI-PASS RECURSIVE BOUNDARY TEST ===\n")
    print("This script pushes the deductive displacement logic through infinite recursion")
    print("until it hits either 99% compression or mathematical diminishing returns.\n")
    
    # 1. TEXT DATA (Highly Structured, low random entropy)
    # Repeating structured data
    text = b"The absolute resonance of deductive logic displaces the threading matrix into pure geometric harmony. " * 300
    run_recursive_test("Text Data (Structured)", text)
    
    # 2. BINARY/IMAGE DATA (Moderate Structure)
    # A mix of structured bytes and small ranges
    binary_data = bytearray()
    for _ in range(30000):
        # Simulating pseudo-structured data like an image map
        binary_data.append(random.randint(50, 100))
    run_recursive_test("Binary / Image Map Data (Moderate Entropy)", binary_data)
    
    # 3. HIGH ENTROPY (Random Noise / Encrypted Data)
    # Pure chaos
    random_data = bytearray(random.getrandbits(8) for _ in range(30000))
    run_recursive_test("Random Noise / Encrypted (High Entropy)", random_data)

if __name__ == "__main__":
    main()
