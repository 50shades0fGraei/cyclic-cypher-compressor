
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sweeper.syllable_generator import CYCLIC_CONSTANT

# --- CCC Engine Library v11.0 ---
# This file provides the core functions for generating cypher streams.

CHARACTER_SET = "abcdefghijklmnopqrstuvwxy"

def _shuffle_list(char_list, sv_int):
    n = len(char_list)
    shuffled_list = char_list[:]
    for i in range(n - 1, 0, -1):
        cyclic_digit = int(CYCLIC_CONSTANT[i % len(CYCLIC_CONSTANT)])
        j = (sv_int + i * cyclic_digit) % (i + 1)
        shuffled_list[i], shuffled_list[j] = shuffled_list[j], shuffled_list[i]
    return shuffled_list

def generate_shuffled_alphabets(sovereign_variables):
    """
    Generates a list of 24 shuffled alphabets, one for each sovereign variable.
    """
    shuffled_alphabets = []
    base_alphabet = list(CHARACTER_SET)
    for sv in sovereign_variables:
        # Convert hex sovereign variable to an integer for the shuffle seed.
        sv_int = int(sv, 16)
        shuffled_alphabet = _shuffle_list(base_alphabet, sv_int)
        shuffled_alphabets.append(''.join(shuffled_alphabet))
    return shuffled_alphabets

def generate_rotor_streams(shuffled_alphabets, length):
    """
    Generates long, repeating streams from the shuffled alphabets to match
    the length of the input content.
    """
    rotor_streams = []
    for alphabet in shuffled_alphabets:
        # Repeat the shuffled alphabet to create a stream of the required length.
        stream = (alphabet * (length // len(alphabet) + 2))[:length]
        rotor_streams.append(stream)
    return rotor_streams
