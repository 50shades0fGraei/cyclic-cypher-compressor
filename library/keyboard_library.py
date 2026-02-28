"""
Keyboard Library - Universal Symbol Reference
Standard keyboard layout: left-to-right ordering
Base characters followed by shift variants
"""

# Standard keyboard symbols left-to-right with shift variants
KEYBOARD_LIBRARY = [
    # Row 1: Number row
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
    # Row 1 Shift variants
    '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
    
    # Row 2: QWERTY row
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
    # Row 2 Shift variants
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|',
    
    # Row 3: ASDF row
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
    # Row 3 Shift variants
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"',
    
    # Row 4: ZXCV row
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
    # Row 4 Shift variants
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?',
    
    # Special characters
    ' ',  # Space
    '\t', # Tab
    '\n', # Newline
]

def get_library():
    """Return the keyboard library as immutable reference"""
    return KEYBOARD_LIBRARY

def get_library_size():
    """Return total symbols in library"""
    return len(KEYBOARD_LIBRARY)

def symbol_to_index(symbol):
    """Map a symbol to its library index"""
    try:
        return KEYBOARD_LIBRARY.index(symbol)
    except ValueError:
        raise ValueError(f"Symbol '{symbol}' not in keyboard library")

def index_to_symbol(index):
    """Map a library index to its symbol"""
    if 0 <= index < len(KEYBOARD_LIBRARY):
        return KEYBOARD_LIBRARY[index]
    raise IndexError(f"Index {index} out of library range (0-{len(KEYBOARD_LIBRARY)-1})")

def get_library_map():
    """Return symbol->index mapping dictionary"""
    return {symbol: idx for idx, symbol in enumerate(KEYBOARD_LIBRARY)}
