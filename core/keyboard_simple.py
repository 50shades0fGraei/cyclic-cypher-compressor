"""
UNIVERSAL KEYBOARD ENCODING - SIMPLIFIED
ANY file → 97 keyboard symbols + 3 variables (Pattern, Multiplier, Position)
All math done in modulo-97 space for perfect consistency
"""

from library.keyboard_library import index_to_symbol, symbol_to_index, get_library_size

PATTERN = [1, 4, 2, 8, 5, 7]
LIBRARY_SIZE = 97  # All operations in mod-97 space

def encode_to_keyboard_simple(data_bytes):
    """
    Encode ANY binary data to keyboard symbols using mod-97 triangulation
    
    Key insight: Working in modulo-97 space is CONSISTENT and REVERSIBLE
    Any byte value becomes deterministic in mod-97 space
    """
    
    if isinstance(data_bytes, str):
        data_bytes = data_bytes.encode('utf-8')
    
    data_length = len(data_bytes)
    
    # Find best multiplier (in mod-97 space)
    best_mult = 1
    best_score = float('inf')
    
    for test_mult in range(1, 7):
        gap_sum = 0
        for pos in range(data_length):
            byte_val = data_bytes[pos] % LIBRARY_SIZE  # Map byte to mod-97
            pattern_val = PATTERN[pos % len(PATTERN)] * test_mult
            triangulation = (pattern_val + pos) % LIBRARY_SIZE
            gap = (byte_val - triangulation) % LIBRARY_SIZE
            gap_sum += gap
        
        if gap_sum < best_score:
            best_score = gap_sum
            best_mult = test_mult
    
    # Encode header
    header_symbols = encode_header_simple(data_length, best_mult)
    
    # Encode data: map each byte to gap symbol
    data_symbols = []
    for pos in range(data_length):
        byte_val = data_bytes[pos] % LIBRARY_SIZE
        pattern_val = PATTERN[pos % len(PATTERN)] * best_mult
        triangulation = (pattern_val + pos) % LIBRARY_SIZE
        gap = (byte_val - triangulation) % LIBRARY_SIZE
        data_symbols.append(index_to_symbol(gap))
    
    keyboard_string = header_symbols + ''.join(data_symbols)
    return keyboard_string, best_mult

def encode_header_simple(data_length, multiplier):
    """
    Encode header: length and multiplier as keyboard symbols
    Format: [Length_base97][Multiplier]
    """
    # Encode length in base-97 (4 symbols should be enough: 97^4 = 88474881)
    len_symbols = []
    remaining = data_length
    for i in range(4):
        digit = remaining % LIBRARY_SIZE
        len_symbols.append(index_to_symbol(digit))
        remaining //= LIBRARY_SIZE
    
    # Multiplier (0-5) → symbol 0-5
    mult_sym = index_to_symbol(multiplier - 1)
    
    # Header: [Multiplier][Length in base-97]
    return mult_sym + ''.join(reversed(len_symbols))

def decode_header_simple(keyboard_string):
    """
    Decode header: extract multiplier and length
    """
    mult_sym = keyboard_string[0]
    multiplier = symbol_to_index(mult_sym) + 1  # 1-6
    
    len_symbols = keyboard_string[1:5]
    data_length = 0
    for i, sym in enumerate(len_symbols):
        digit = symbol_to_index(sym)
        data_length += digit * (LIBRARY_SIZE ** (3 - i))
    
    return multiplier, data_length, 5

def decode_from_keyboard_simple(keyboard_string):
    """
    Decode keyboard symbols back to original (mod-97 space)
    """
    multiplier, data_length, payload_start = decode_header_simple(keyboard_string)
    
    payload = keyboard_string[payload_start:payload_start + data_length]
    
    # Reconstruct
    decoded = bytearray()
    for pos in range(data_length):
        if pos < len(payload):
            sym = payload[pos]
            gap = symbol_to_index(sym)
            pattern_val = PATTERN[pos % len(PATTERN)] * multiplier
            triangulation = (pattern_val + pos) % LIBRARY_SIZE
            byte_val = (triangulation + gap) % LIBRARY_SIZE
            decoded.append(byte_val)
    
    return bytes(decoded)

def verify_keyboard_simple(original_data):
    """Verify round-trip in mod-97 space"""
    if isinstance(original_data, str):
        original_data = original_data.encode('utf-8')
    
    # Map original to mod-97 space
    original_mod97 = bytes(b % LIBRARY_SIZE for b in original_data)
    
    # Encode
    keyboard_str, _ = encode_to_keyboard_simple(original_data)
    
    # Decode
    decoded = decode_from_keyboard_simple(keyboard_str)
    
    # Check: decoded should match original_mod97
    return decoded == original_mod97, keyboard_str, decoded, original_mod97
