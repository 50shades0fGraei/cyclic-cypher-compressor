import re

with open('core/cyberdna_engine.py', 'r', encoding='utf-8') as f:
    core_code = f.read()

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

core_code = re.sub(r'    def decompress\(self, input_path, output_path\):.*', decompress_new, core_code, flags=re.DOTALL)

with open('core/cyberdna_engine.py', 'w', encoding='utf-8') as f:
    f.write(core_code)
