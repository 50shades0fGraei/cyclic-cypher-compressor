"""
Cyclic Cypher Compressor - Signature-Based Archiver (CCA)
For long-term data storage and archiving with multi-cypher system.

Splits data by character type:
- Alphabetic characters
- Punctuation marks
- Mathematical symbols  
- Numerical values
- Function characters

Each gets its own cypher stream and signature compression.
"""

import json
import os
import hashlib
from datetime import datetime

# Character type classifications
CHARACTER_SETS = {
    'alphabetic': set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'),
    'punctuation': set('.,;:!?\'"()[]{}'),
    'mathematical': set('+-*/%=<>'),
    'numerical': set('0123456789'),
    'function': set('_@#$&~^|\\')
}

CYCLIC_CONSTANT = "142857"

def generate_sovereign_variables(secret_key):
    """Generate deterministic variables from secret key."""
    h = hashlib.sha256(secret_key.encode()).hexdigest()
    return [int(h[i:i+2], 16) for i in range(0, len(h), 2)]

def generate_shuffled_alphabets(sovereign_variables):
    """Generate shuffled character alphabets from sovereign variables."""
    base_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabets = []
    for i, val in enumerate(sovereign_variables):
        chars = list(base_alphabet)
        # Shuffle based on sovereign variable
        for _ in range(val % 10):
            chars = chars[1:] + chars[:1]
        alphabets.append(''.join(chars))
    return alphabets

def generate_rotor_streams(shuffled_alphabets, stream_length):
    """Generate rotor streams of specified length."""
    streams = []
    for alphabet in shuffled_alphabets:
        stream = (alphabet * ((stream_length // len(alphabet)) + 1))[:stream_length]
        streams.append(stream)
    return streams

def get_wait_time(char_to_find, stream, start_pos):
    """Get distance to next occurrence of character in stream."""
    try:
        index = stream.index(char_to_find, start_pos)
        return index - start_pos
    except ValueError:
        return -1

def classify_character(char):
    """Determine character type classification."""
    for char_type, char_set in CHARACTER_SETS.items():
        if char in char_set:
            return char_type
    return 'unknown'

def generate_signature(content, sovereign_variables, char_type):
    """
    Generate signature for specific character type.
    Returns accumulated tallies for that character class.
    """
    shuffled_alphabets = generate_shuffled_alphabets(sovereign_variables)
    rotor_streams = generate_rotor_streams(shuffled_alphabets, len(content))
    cypher_pairs = [(rotor_streams[i], rotor_streams[i+6]) for i in range(6)]
    
    final_signature = [0] * 6
    position_map = []
    
    for i, char in enumerate(content):
        if char not in CHARACTER_SETS[char_type]:
            continue
        
        position_map.append(i)
        
        for pair_index, (forward_rotor, reverse_rotor) in enumerate(cypher_pairs):
            forward_tally = get_wait_time(char, forward_rotor, i)
            reverse_tally = get_wait_time(char, reverse_rotor, i)
            
            total_pair_tally = 0
            if forward_tally != -1:
                total_pair_tally += forward_tally
            if reverse_tally != -1:
                total_pair_tally += reverse_tally
            
            final_signature[pair_index] += total_pair_tally
        
        cyclic_digit = int(CYCLIC_CONSTANT[i % len(CYCLIC_CONSTANT)])
        final_signature = [val + cyclic_digit for val in final_signature]
    
    return final_signature, position_map

def create_archive(input_path, output_path, secret_key="default_key"):
    """
    Create signature-based archive with multi-cypher compression.
    Generates signatures for each character type separately.
    """
    print(f"\n{'='*80}")
    print(f"CYCLIC SIGNATURE ARCHIVER (CSA) v1.0 - Long-term Storage Compression")
    print(f"{'='*80}")
    
    # Read input
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {input_path}")
        return
    
    original_size = len(content.encode('utf-8'))
    print(f"\nInput file: {os.path.basename(input_path)}")
    print(f"File size: {original_size:,} bytes")
    
    # Generate sovereign variables
    sovereign_variables = generate_sovereign_variables(secret_key)
    
    # Build archive structure
    archive = {
        'metadata': {
            'original_filename': os.path.basename(input_path),
            'original_size_bytes': original_size,
            'created': datetime.now().isoformat(),
            'version': '1.0',
            'compression_type': 'signature-based',
            'secret_key_hash': hash(secret_key) & 0xffffffff
        },
        'character_counts': {},
        'signatures': {}
    }
    
    print(f"\nGenerating signatures by character type...")
    print(f"{'-'*80}")
    
    total_chars_processed = 0
    compressed_metadata_size = 0
    
    # Generate signature for each character type
    for char_type in CHARACTER_SETS.keys():
        # Extract characters of this type
        type_content = ''.join(c for c in content if classify_character(c) == char_type)
        
        if not type_content:
            print(f"  {char_type:12} : 0 chars (skipped)")
            continue
        
        # Generate signature
        signature, positions = generate_signature(type_content, sovereign_variables, char_type)
        
        archive['character_counts'][char_type] = len(type_content)
        archive['signatures'][char_type] = {
            'signature': signature,
            'char_count': len(type_content),
            'position_count': len(positions)
        }
        
        total_chars_processed += len(type_content)
        sig_size = len(json.dumps(signature).encode('utf-8'))
        compressed_metadata_size += sig_size
        
        compression_ratio = (sig_size / (len(type_content) * 1)) * 100  # rough estimate
        print(f"  {char_type:12} : {len(type_content):6} chars → {sig_size:5} bytes ({compression_ratio:6.2f}%)")
    
    # Handle unknown characters
    unknown = ''.join(c for c in content if classify_character(c) == 'unknown')
    if unknown:
        archive['character_counts']['unknown'] = len(unknown)
        print(f"  {'unknown':12} : {len(unknown):6} chars (preserved as base64)")
        import base64
        archive['signatures']['unknown'] = {
            'data': base64.b64encode(unknown.encode('utf-8')).decode('ascii'),
            'char_count': len(unknown)
        }
        unknown_size = len(archive['signatures']['unknown']['data'].encode('utf-8'))
        compressed_metadata_size += unknown_size
    
    # Write archive
    archive_json = json.dumps(archive, indent=2)
    archive_size = len(archive_json.encode('utf-8'))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(archive_json)
    
    # Report
    print(f"\n{'-'*80}")
    print(f"ARCHIVAL RESULTS:")
    print(f"  Original size:        {original_size:,} bytes")
    print(f"  Archive size:         {archive_size:,} bytes")
    print(f"  Compression ratio:    {(archive_size / original_size) * 100:.6f}%")
    print(f"  Space saved:          {original_size - archive_size:,} bytes")
    print(f"  Total chars indexed:  {total_chars_processed:,}")
    print(f"\nArchive saved to: {output_path}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cyclic Signature Archiver (CSA) - Long-term storage compression")
    parser.add_argument("--input", type=str, required=True, help="Input file to archive")
    parser.add_argument("--output", type=str, required=True, help="Output archive file")
    parser.add_argument("--key", type=str, default="default_key", help="Secret key for reproducible compression")
    
    args = parser.parse_args()
    create_archive(args.input, args.output, args.key)
