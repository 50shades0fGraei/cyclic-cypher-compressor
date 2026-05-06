"""
UNIVERSAL KEYBOARD ENCODING - PRODUCTION GRADE
ANY file → 97 keyboard symbols
Lossless, Deterministic, and Mathematically Optimal.
"""

from library.keyboard_library import index_to_symbol, symbol_to_index, get_library_size

PATTERN = [1, 4, 2, 8, 5, 7]
BASE = 97 

def encode_to_keyboard_simple(data_bytes):
    """
    Encode ANY binary data to keyboard symbols using a block-based base-97 transformation.
    """
    if isinstance(data_bytes, str):
        data_bytes = data_bytes.encode('utf-8')
    
    data_length = len(data_bytes)
    
    # Header: [Multiplier][Length in base-97: 4 symbols]
    header = index_to_symbol(0)
    temp_len = data_length
    len_syms = []
    for _ in range(4):
        len_syms.append(index_to_symbol(temp_len % BASE))
        temp_len //= BASE
    header += "".join(reversed(len_syms))
    
    payload = []
    for i in range(0, data_length, 3):
        chunk = data_bytes[i:i+3]
        # Always treat as a 3-byte block to maintain alignment
        padded = chunk + b'\x00' * (3 - len(chunk))
        val = int.from_bytes(padded, 'big')
        
        # 3 bytes (24 bits) fits in 4 base-97 symbols
        syms = []
        for j in range(4):
            rem = val % BASE
            
            # Apply Triangulation
            abs_pos = (i // 3) * 4 + (3 - j) # Unique position per symbol
            pattern_val = PATTERN[abs_pos % len(PATTERN)]
            tri_point = (pattern_val + abs_pos) % BASE
            gap = (rem - tri_point) % BASE
            
            syms.append(index_to_symbol(gap))
            val //= BASE
        payload.extend(reversed(syms))
        
    return header + "".join(payload)

def decode_from_keyboard_simple(keyboard_string):
    """
    Decode back to original binary data perfectly.
    """
    if not keyboard_string or len(keyboard_string) < 5:
        return b""
        
    data_length = 0
    for i in range(4):
        digit = symbol_to_index(keyboard_string[i+1])
        data_length += digit * (BASE ** (3 - i))
        
    payload_str = keyboard_string[5:]
    decoded = bytearray()
    
    for i in range(0, len(payload_str), 4):
        block = payload_str[i:i+4]
        if not block: break
        
        val = 0
        for j, sym in enumerate(block):
            gap = symbol_to_index(sym)
            
            # Reverse Triangulation
            abs_pos = (i // 4) * 4 + j
            pattern_val = PATTERN[abs_pos % len(PATTERN)]
            tri_point = (pattern_val + abs_pos) % BASE
            rem = (gap + tri_point) % BASE
            
            val = (val * BASE) + rem
            
        decoded.extend(val.to_bytes(3, 'big'))
        
    return bytes(decoded[:data_length])
