# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

import os
import struct
import zlib
import time

class VideoCompressor:
    """
    Personal Video Compression Engine (Deductive Metronome).
    Optimized for personal storage with high density.
    """
    
    def __init__(self, pattern=[1, 4, 2, 8, 5, 7], chunk_size=1024 * 1024):
        self.pattern = pattern
        self.chunk_size = chunk_size

    def encode_chunk(self, chunk):
        orig_len = len(chunk)
        processed_mask = bytearray(orig_len)
        
        packed = bytearray(struct.pack('<I', orig_len))
        pattern_data = bytearray()
        num_patterns = 0

        # null-Space (Deductive Zero-Point)
        zero_positions = [i for i, b in enumerate(chunk) if b == 0]
        if zero_positions:
            num_patterns += 1
            pattern_data.append(0) # Cypher 0
            pattern_data.append(0) # Multiplier 0
            pattern_data.extend(struct.pack('<I', len(zero_positions)))
            last_pos = -1
            for pos in zero_positions:
                gap = pos - last_pos
                if gap < 254:
                    pattern_data.append(gap)
                else:
                    pattern_data.append(255)
                    pattern_data.extend(struct.pack('<I', gap))
                processed_mask[pos] = 1
                last_pos = pos

        # Metronome Sweep (Cycles 1-6)
        for m in range(1, 7):
            matches = {}
            for pos in range(orig_len):
                if processed_mask[pos]: continue
                byte_val = chunk[pos]
                metronome_val = (self.pattern[pos % 6] * m) % 256
                if metronome_val == byte_val:
                    if byte_val not in matches: matches[byte_val] = []
                    matches[byte_val].append(pos)
            
            for byte_val, positions in sorted(matches.items(), key=lambda x: len(x[1]), reverse=True):
                # Only process if there are enough matches to justify the overhead
                valid_positions = [p for p in positions if not processed_mask[p]]
                if not valid_positions: continue
                
                num_patterns += 1
                pattern_data.append(byte_val)
                pattern_data.append(m)
                pattern_data.extend(struct.pack('<I', len(valid_positions)))
                
                last_pos = -1
                for pos in valid_positions:
                    gap = pos - last_pos
                    if gap < 254:
                        pattern_data.append(gap)
                    else:
                        pattern_data.append(255)
                        pattern_data.extend(struct.pack('<I', gap))
                    processed_mask[pos] = 1
                    last_pos = pos

        packed.extend(struct.pack('<H', num_patterns))
        packed.extend(pattern_data)
        
        # Residuals
        residual_string = bytearray([chunk[p] for p in range(orig_len) if not processed_mask[p]])
        if residual_string:
            packed.extend(zlib.compress(residual_string, 9))
            
        return packed

    def decode_chunk(self, packed_data):
        orig_len = struct.unpack('<I', packed_data[0:4])[0]
        num_patterns = struct.unpack('<H', packed_data[4:6])[0]
        
        chunk = bytearray(orig_len)
        processed_mask = bytearray(orig_len)
        ptr = 6
        
        for _ in range(num_patterns):
            cypher = packed_data[ptr]
            multiplier = packed_data[ptr + 1]
            count = struct.unpack('<I', packed_data[ptr + 2 : ptr + 6])[0]
            ptr += 6
            
            last_pos = -1
            for _ in range(count):
                flag = packed_data[ptr]
                ptr += 1
                if flag < 254:
                    gap = flag
                else:
                    gap = struct.unpack('<I', packed_data[ptr : ptr + 4])[0]
                    ptr += 4
                
                pos = last_pos + gap
                if pos < orig_len:
                    chunk[pos] = cypher
                    processed_mask[pos] = 1
                last_pos = pos
        
        if ptr < len(packed_data):
            residual_string = zlib.decompress(packed_data[ptr:])
            res_idx = 0
            for p in range(orig_len):
                if not processed_mask[p] and res_idx < len(residual_string):
                    chunk[p] = residual_string[res_idx]
                    res_idx += 1
                    
        return chunk

    def compress(self, input_path, output_path):
        file_size = os.path.getsize(input_path)
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            fout.write(b'PVV6') # Personal Video Vault V6
            fout.write(struct.pack('<Q', file_size))
            while True:
                chunk = fin.read(self.chunk_size)
                if not chunk: break
                packed = self.encode_chunk(chunk)
                fout.write(struct.pack('<I', len(packed)))
                fout.write(packed)
        return output_path

    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            magic = fin.read(4)
            if magic != b'PVV6': raise ValueError("Invalid Personal Vault Header")
            orig_total = struct.unpack('<Q', fin.read(8))[0]
            while True:
                header = fin.read(4)
                if not header: break
                packed_len = struct.unpack('<I', header)[0]
                packed_body = fin.read(packed_len)
                fout.write(self.decode_chunk(packed_body))
        return output_path
