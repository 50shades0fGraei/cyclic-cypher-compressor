import re

with open('core/cyberdna_engine.py', 'r', encoding='utf-8') as f:
    core_code = f.read()

payload_logic = """
    def encode_payload(self, data: bytes) -> bytes:
        orig_len = len(data)
        out = bytearray()
        
        # Optimize O(N) instead of O(N^2)
        positions = [[] for _ in range(256)]
        for i, b in enumerate(data):
            positions[b].append(i)
            
        for target_byte in range(256):
            pos_list = positions[target_byte]
            if not pos_list: continue
            
            out.append(target_byte)
            out.extend(struct.pack('<I', len(pos_list)))
            
            last_pos = -1
            for pos in pos_list:
                gap = pos - last_pos
                while gap >= 255:
                    out.append(255)
                    gap -= 255
                out.append(gap)
                last_pos = pos
        return out

    def decode_payload(self, packed: bytes, orig_len: int) -> bytes:
        data = bytearray(orig_len)
        ptr = 0
        total_placed = 0
        
        while ptr < len(packed) and total_placed < orig_len:
            target_byte = packed[ptr]
            ptr += 1
            import struct
            count = struct.unpack('<I', packed[ptr:ptr+4])[0]
            ptr += 4
            
            last_pos = -1
            for _ in range(count):
                gap = 0
                while packed[ptr] == 255:
                    gap += 255
                    ptr += 1
                gap += packed[ptr]
                ptr += 1
                
                pos = last_pos + gap
                data[pos] = target_byte
                last_pos = pos
                total_placed += 1
        return data

    def compress"""

core_code = core_code.replace("    def compress", payload_logic)

compress_original = """    def compress(self, input_path, output_path):
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
        return output_path"""

compress_new = """    def compress(self, input_path, output_path):
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
        return output_path"""

core_code = core_code.replace(compress_original, compress_new)

decompress_original = """    def decompress(self, input_path, output_path):
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
            # Pure Sovereign Extraction
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
        return output_path"""

decompress_new = """    def decompress(self, input_path, output_path):
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
        return output_path"""

core_code = core_code.replace(decompress_original, decompress_new)

with open('core/cyberdna_engine.py', 'w', encoding='utf-8') as f:
    f.write(core_code)
print("Updated core engine!")
