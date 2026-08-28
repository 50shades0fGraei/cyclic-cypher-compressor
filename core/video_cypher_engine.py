import numpy as np

ETERNAL_MATRIX = [1, 4, 2, 8, 5, 7]
MULTIPLIER_MATRICES = [
    [1, 4, 2, 8, 5, 7], 
    [2, 8, 5, 7, 1, 4], 
    [4, 2, 8, 5, 7, 1], 
    [5, 7, 1, 4, 2, 8], 
    [7, 1, 4, 2, 8, 5], 
    [8, 5, 7, 1, 4, 2], 
    [9, 9, 9, 9, 9, 9]  
]

def map_byte_to_matrix(byte_val: int):
    c_group = byte_val // 6
    matrix_value = ETERNAL_MATRIX[byte_val % 6]
    return c_group, matrix_value

class VideoCypherStage1:
    def encode_chunk(self, chunk: bytes) -> str:
        orig_len = len(chunk)
        freq = {c: {m: {'anchor': None, 'sums': [0]*6} for m in range(6)} for c in range(43)}
        
        for i, b in enumerate(chunk):
            c_group, m_int = map_byte_to_matrix(b)
            cycle_beat = i % 6
            lineal_cycle = i // 6
            
            for m_idx in range(6):
                if m_int == MULTIPLIER_MATRICES[m_idx][cycle_beat]:
                    slot = ETERNAL_MATRIX.index(m_int)
                    if freq[c_group][m_idx]['anchor'] is None:
                        freq[c_group][m_idx]['anchor'] = lineal_cycle
                    freq[c_group][m_idx]['sums'][slot] += 1
                    break
                    
        parts = [str(orig_len)]
        for c in range(43):
            for m in range(6):
                if freq[c][m]['anchor'] is not None:
                    anchor = freq[c][m]['anchor']
                    sums = freq[c][m]['sums']
                    s_str = ".".join(map(str, sums))
                    parts.append(f"{c}.{m+1}.{anchor}.{s_str}")
        return '|'.join(parts)

    def decode_chunk(self, encoded: str) -> bytes:
        parts = encoded.split('|')
        orig_len = int(parts[0])
        matrix = [None] * orig_len
        
        blocks = []
        for part in parts[1:]:
            if not part: continue
            nums = [int(x) for x in part.split('.')]
            c = nums[0]
            m_idx = nums[1] - 1
            anchor = nums[2]
            sums = nums[3:]
            blocks.append((c, m_idx, anchor, sums))
            
        blocks.sort(key=lambda x: x[0], reverse=True)
        
        for c, m_idx, anchor, sums in blocks:
            active_matrix = MULTIPLIER_MATRICES[m_idx]
            for slot_idx, count in enumerate(sums):
                if count == 0: continue
                target_int = ETERNAL_MATRIX[slot_idx]
                byte_val = (c * 6) + slot_idx
                beat_offset = active_matrix.index(target_int)
                
                placed = 0
                search_idx = (anchor * 6) + beat_offset
                while placed < count and search_idx < orig_len:
                    if matrix[search_idx] is None:
                        matrix[search_idx] = byte_val
                        placed += 1
                    search_idx += 6 

        return bytes([v if v is not None else 0 for v in matrix])

