
import argparse
import os

# The six multipliers that form the core of the compression sweep.
MULTIPLIERS = [f"x{i}" for i in range(1, 7)]

def chunk_data(data, chunk_size):
    """Breaks data into chunks of a specified size."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def find_best_multiplier(chunk):
    """
    Analyzes a chunk and determines the best multiplier.
    
    This is the core of the "sweep" logic. For now, we will simulate this
    by assigning a multiplier based on a simple hash of the chunk. This
    creates a deterministic, but non-optimized, mapping.
    """
    # A simple, deterministic way to choose a multiplier for a chunk.
    chunk_hash = sum(ord(c) for c in chunk)
    multiplier_index = chunk_hash % len(MULTIPLIERS)
    return MULTIPLIERS[multiplier_index]

def sweep_and_compress(input_file, output_file, chunk_size):
    """
    Performs the multi-pass sweep to generate a compressed instruction set.
    """
    print(f"--- Starting Compression Sweep for {input_file} ---")
    
    try:
        with open(input_file, 'r') as f:
            coordinate_data = f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_file}")
        return

    print(f"1. Breaking coordinate data into chunks of {chunk_size} characters...")
    chunks = chunk_data(coordinate_data, chunk_size)
    print(f"   - Total Chunks: {len(chunks)}")

    print("2. Determining best multiplier for each chunk...")
    instruction_set = [find_best_multiplier(chunk) for chunk in chunks]

    print(f"3. Saving compressed instruction set to {output_file}...")
    with open(output_file, 'w') as f:
        # Save as a comma-separated string, which is highly efficient.
        f.write(",".join(instruction_set))
    
    print("\n--- Compression Sweep Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress a translated coordinate file into a multiplier instruction set."
    )
    parser.add_argument(
        "--input", 
        type=str, 
        required=True, 
        help="The translated coordinate file to compress."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="archive/compressed_set.ccc",
        help="The name of the final compressed file."
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=24,
        help="The segment size for pattern analysis (e.g., 24)."
    )
    args = parser.parse_args()

    # Ensure the output directory exists.
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    sweep_and_compress(args.input, args.output, args.chunksize)
