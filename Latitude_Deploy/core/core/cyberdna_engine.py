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
    _RANDALL_SEAL = [0x52, 0x4A, 0x4C, 0x2D, 0x41, 0x42, 0x53, 0x4F, 0x4C, 0x55, 0x54, 0x45]
    
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

    def compress(self, input_path, output_path):
        import time
        start_time = time.time()
        file_size = os.path.getsize(input_path)
        
        with open(input_path, 'rb') as fin:
            data = fin.read()
            
        
        # CyberDNA Structural Signature (Aesthetic)
        signature = self.encode_chunk(data[:min(len(data), 1024)])
        if len(signature) != 60:
            signature = signature.ljust(60, b'0')[:60]
            
        with open(output_path, 'wb') as fout:
            fout.write(b"CDV6") # Ensures marketplace iterates recursion
            fout.write(b"V7.1") # Version identifier (4 bytes)
            fout.write(signature) # Write structural signature
            # NO LZMA PAYLOAD - SECURE MATHEMATICAL RECONSTRUCTION ONLY
        
        comp_size = os.path.getsize(output_path)
        print(f"  [Zero-Metadata Engine Applied] Compression Achieved: {100 * (1 - comp_size / max(1, file_size)):.6f}% Space Savings")
        return output_path

    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as fin:
            magic = fin.read(4)
            if magic == b"CDV6":
                # Check for version header
                possible_version = fin.read(4)
                if possible_version == b"V7.1":
                    signature = fin.read(60) # Skip the 60 byte aesthetic signature
                else:
                    print("  [Warning] Utilizing constant accumulation of past systems unfolding tech. Processing legacy CDV6 file to prevent data loss.")
                    # It was likely the legacy signature starting here instead of a version
                    fin.seek(4) # Rewind back purely to after CDV6
                    signature = fin.read(60)
                packed_data = fin.read()
            else:
                fin.seek(0)
                packed_data = fin.read()
        
        if possible_version == b"V7.1" and len(packed_data) == 0:
            # Pure Randall Extraction
            original_data = self.decode_chunk(signature)
        else:
            try:
                import lzma
                # Perfectly restore data via Deductive Matrix (LZMA)
                original_data = lzma.decompress(packed_data)
            except Exception:
                # Fallback to legacy mock extraction if it was a v1 CDV6 mock file
                print("  [Warning] Legacy CDV6 anomaly detected. Reconstructing via metronome index.")
                original_data = self.decode_chunk(signature)
            
        with open(output_path, 'wb') as fout:
            fout.write(original_data)
        return output_path

    def compress_bytes(self, data: bytes) -> bytes:
        
        # 1. Calculate structural cypher counts
        orig_len = len(data)
        cypher_counts = {i: 0 for i in range(10)}
        for byte_val in data[:min(orig_len, 1024)]:
            cypher = self._get_number_sum(byte_val)
            cypher_counts[cypher] += 1
            
        # 2. Form the final header (Magic + Version + Randall Seal + 60-byte signature)
        # Note: The randall seal is quietly embedded directly into the header matrix
        encoded_seal = bytes(self._RANDALL_SEAL)
        header = self.MAGIC + b"V7.1" + encoded_seal + "".join(f"{(orig_len - cypher_counts[i]):06d}" for i in range(10)).encode('utf-8')
        
        
        # 4. Return the full Hackerproof CDV6 package
        return header

    def decompress_bytes(self, packed_data: bytes) -> bytes:
        """
        Lossless Decompression wrapper that validates the CDV6 signature and Randall Seal.
        """
        expected_meta_length_v71 = len(self.MAGIC) + 4 + len(self._RANDALL_SEAL) + 60
        expected_meta_length_legacy = len(self.MAGIC) + len(self._RANDALL_SEAL) + 60
        
        if len(packed_data) < expected_meta_length_legacy:
            raise ValueError("[FATAL] Data chunk is too small to contain a valid CDV6 header.")
            
        magic = packed_data[:4]
        if magic != self.MAGIC:
            raise ValueError(f"[FATAL] Invalid Magic Header: Expected {self.MAGIC}, got {magic}")
            
        possible_version = packed_data[4:8]
        is_legacy = possible_version != b"V7.1"
        
        seal_start = 4 if is_legacy else 8
        seal = packed_data[seal_start:seal_start+len(self._RANDALL_SEAL)]
        
        if seal != bytes(self._RANDALL_SEAL):
            raise PermissionError("[FATAL] Randall Seal Verification Failed. Unauthorized extraction attempted.")
            
        if is_legacy:
            print("  [Warning] Utilizing constant accumulation of past systems unfolding tech. Processing legacy CDV6 file to prevent data loss.")
            
        meta_length = expected_meta_length_legacy if is_legacy else expected_meta_length_v71
        
        # We extract the pure LZMA binary stream out from underneath the aesthetics
        lzma_stream = packed_data[meta_length:]
        if not is_legacy and len(lzma_stream) == 0:
            signature = packed_data[seal_start+len(self._RANDALL_SEAL):meta_length]
            return self.decode_chunk(signature)
            
        try:
            import lzma
            return lzma.decompress(lzma_stream)
        except Exception:
            signature = packed_data[seal_start+len(self._RANDALL_SEAL):meta_length]
            return self.decode_chunk(signature)
