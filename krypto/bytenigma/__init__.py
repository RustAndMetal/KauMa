from typing import List
from krypto.actions import action
from .rotors import rotors_encrypt, rotor_reverse_init, turn_rotors

@action("bytenigma")
def bytenigma(rotors, input) -> bytes:
    # init reverse rotors
    reverse_rotors = rotor_reverse_init(rotors)
    final_output = []
    turn_list: List[int] = [0] * len(rotors)
    # send input(single byte) through rotors
    for byte in input:
        # returns one encrypted byte int
        output = rotors_encrypt(rotors, reverse_rotors, turn_list, byte)
        # append output to output list
        final_output.append(output)
        # turn rotors
        turn_rotors(rotors, turn_list)
        
    return bytes(final_output)
