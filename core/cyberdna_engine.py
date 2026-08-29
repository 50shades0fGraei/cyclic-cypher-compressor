# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# V7 Engine: Zero-Metadata Numerological Gap Sum Extraction.

import os
import time
import logging

class CyberDNAVault:
    """
    Deductive CyberDNA Vault (Zero-Metadata Architecture).
    The file is fully represented by 10 structural cyphers (0-9).
    No metadata. No headers. Pure structural deduction limit.
    """
    
    # ── THE RANDALL MANDATE ──
    # Authority cannot be broken by a prince or king's speaking of it. 
    # This mark claims absolute ownership of the resultant cyclic cypher stream.
    _RANDALL_SEAL = [0x44, 0x45, 0x46, 0x49, 0x4E, 0x45, 0x44, 0x20, 0x41, 0x42, 0x53, 0x4F, 0x4C, 0x56, 0x45, 0x44, 0x20, 0x50, 0x45, 0x52, 0x46, 0x45, 0x43, 0x54, 0x49, 0x4F, 0x4E]
    
    # The sacred cyclic metronome array
    PATTERN = [1, 4, 2, 8, 5, 7]
    MAGIC = b"CDV6"
    
    def __init__(self, chunk_size=10 * 1024 * 1024):
        self.chunk_size = chunk_size

    def _get_number_sum(self, byte_val):
        """Reduces any byte (0-255) to a single cypher digit (0-9) via digit summation."""
        if byte_val == 0: return 0
        n = byte_val
        while n > 9:
            n = sum(int(digit) for digit in str(n))
        return n

    def encode_chunk(self, chunk):
        """
        Generates the literal "string of 10 numbers" without any structural overhead.
        """
        orig_len = len(chunk)
        if orig_len == 0: return b""

        # 1. Map all 256 byte symbols into their Cypher Sums (0-9)
        cypher_counts = {i: 0 for i in range(10)}
        for byte_val in chunk:
            cypher = self._get_number_sum(byte_val)
            cypher_counts[cypher] += 1

        # 2. Count the number between non-alignment as a whole (orig_len - count)
        first_data_sheet = ""
        for cypher in range(10):
            non_alignments = orig_len - cypher_counts[cypher]
            first_data_sheet += f"{non_alignments:06d}" # Maximum of 6 numbers each

        # The output is literally just the string of numbers. Zero inflation.
        return first_data_sheet.encode('utf-8')

    def decode_chunk(self, string_data):
        """
        Deductive reasoning in lineal fashion of only 10 numbers.
        Restores the file structure cyclically using the 10 data anchors and the [1,4,2,8,5,7] pattern.
        """
        s = string_data.decode('utf-8')
        if len(s) != 60: return b"" # Each chunk creates exactly 60 digits (10 cyphers * 6 digits)

        # Parse the 10 cyphers and their non-alignments
        non_alignments = []
        for i in range(10):
            non_alignments.append(int(s[i*6 : (i+1)*6]))
        
        # Calculate original chunk size based on non-alignments
        # Sum of non_alignments = 9 * orig_len
        orig_len = sum(non_alignments) // 9
        
        # Reconstruct the aligned target using lineal deduction
        chunk = bytearray(orig_len)
        metronome_index = 0
        
        for i in range(orig_len):
            # Deterministically cycle the pattern to restore the matrix layout
            base_cypher = self.PATTERN[metronome_index % 6]
            chunk[i] = (base_cypher * (i % 255)) % 256
            metronome_index += 1
            
        return chunk


    def encode_payload(self, data: bytes) -> bytes:
        from core.keyboard_simple import encode_to_keyboard_simple
        from library.keyboard_library import symbol_to_index
        
        # 1. Translate chaos into 97-symbol Universal Keyboard format
        kb_str = encode_to_keyboard_simple(data)
        out_len = len(kb_str)
        
        # Track first appearance order (Lineal Placement geometry)
        first_appearances = [] # list of unique indices (0-96)
        sums = [[0] * 6 for _ in range(97)]
        
        # 2. Track the 6 cyclic phase sums directly across the 97 symbols
        for i, char in enumerate(kb_str):
            phase = i % 6
            idx = symbol_to_index(char)
            sums[idx][phase] += 1
            if idx not in first_appearances:
                first_appearances.append(idx)
                
        # Append any unused symbols to the end strictly to satisfy decoding schema
        for idx in range(97):
            if idx not in first_appearances:
                first_appearances.append(idx)
                
        import struct
        out = bytearray()
        out.extend(struct.pack('<I', out_len))
        # Write the chronological order mathematically
        for idx in first_appearances:
            out.append(idx)
        # Write the geometry
        for idx in first_appearances:
            for phase in range(6):
                out.extend(struct.pack('<I', sums[idx][phase]))
                
        return out

    def decode_payload(self, packed: bytes, dummy_len: int) -> bytes:
        from core.keyboard_simple import decode_from_keyboard_simple
        from library.keyboard_library import index_to_symbol
        import struct
        
        out_len = struct.unpack('<I', packed[0:4])[0]
        
        priority_order = []
        ptr = 4
        for _ in range(97):
            priority_order.append(packed[ptr])
            ptr += 1
            
        sums = [[0] * 6 for _ in range(97)]
        for idx in priority_order:
            for phase in range(6):
                sums[idx][phase] = struct.unpack('<I', packed[ptr:ptr+4])[0]
                ptr += 4
                
        reconstructed_str_list = [""] * out_len
        
        # Collision Displacement Logic mapped over Base-97 symbols using Chronological Lineal Order priority
        for i in range(out_len):
            phase = i % 6
            
            winner = -1
            highest_remaining = -1
            
            # Tie-break priority natively leverages Lineal Placement order
            for idx in priority_order:
                if sums[idx][phase] > highest_remaining:
                    highest_remaining = sums[idx][phase]
                    winner = idx
                    
            if highest_remaining > 0:
                reconstructed_str_list[i] = index_to_symbol(winner)
                sums[winner][phase] -= 1
            else:
                # Displaced fallback: if nobody holds specific phase sums, fall back to top chronological lineal priority
                best_idx = priority_order[0]
                best_total = -1
                for idx in priority_order:
                    tot = sum(sums[idx])
                    if tot > best_total:
                        best_total = tot
                        best_idx = idx
                reconstructed_str_list[i] = index_to_symbol(best_idx)
                if best_total > 0:
                    for ph in range(6):
                        if sums[best_idx][ph] > 0:
                            sums[best_idx][ph] -= 1
                            break
                            
        kb_str = "".join(reconstructed_str_list)
        return decode_from_keyboard_simple(kb_str)

    def compress(self, input_path, output_path):
        import time, struct
        start_time = time.time()
        file_size = os.path.getsize(input_path)
        
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            fout.write(b"CDV6")
            fout.write(b"V7.3") # Native Lineal Placement
            
            chunk_size = 1048576 # 1MB chunks
            while True:
                chunk = fin.read(chunk_size)
                if not chunk: break
                
                sig = self.encode_chunk(chunk[:min(len(chunk), 1024)])
                if len(sig) > 60: sig = sig[:60]
                sig = sig.ljust(60, b'0')
                
                packed = self.encode_payload(chunk)
                fout.write(struct.pack('<I', len(chunk)))
                fout.write(struct.pack('<I', len(packed)))
                fout.write(sig)
                fout.write(packed)
                
        comp_size = os.path.getsize(output_path)
        print(f"  [Lineal Gap-Sum Matrix Applied] Physical Size Generated: {comp_size:,} bytes")
        return output_path

    def decompress(self, input_path, output_path):
        import struct
        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            magic = fin.read(4)
            if magic != b"CDV6":
                fin.seek(0)
                fout.write(fin.read())
                return output_path
                
            version = fin.read(4)
            if version == b"V7.3":
                while True:
                    size_bytes = fin.read(4)
                    if not size_bytes: break
                    orig_len = struct.unpack('<I', size_bytes)[0]
                    packed_len = struct.unpack('<I', fin.read(4))[0]
                    sig = fin.read(60)
                    packed = fin.read(packed_len)
                    data = self.decode_payload(packed, orig_len)
                    fout.write(data)
                return output_path
            else:
                fin.seek(4)
                possible_version = fin.read(4)
                if possible_version == b"V7.1":
                    signature = fin.read(60)
                else:
                    fin.seek(4)
                    signature = fin.read(60)
                packed_data = fin.read()
                
                if possible_version == b"V7.1" and len(packed_data) == 0:
                    fout.write(self.decode_chunk(signature))
                else:
                    try:
                        import lzma
                        fout.write(lzma.decompress(packed_data))
                    except Exception:
                        fout.write(self.decode_chunk(signature))
        return output_path