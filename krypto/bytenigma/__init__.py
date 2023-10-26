from typing import List
from krypto.actions import action
from .rotors import rotors_encrypt, rotor_reverse_init, turn_rotors

@action("bytenigma")
def bytenigma(rotors: List[List[int]], input: bytes) -> bytes:
    """Encrypts the input with the given rotors

    Args:
        rotors (List[List[int]]): A list of lists representing the rotors to be used for encryption
        input (bytes): The input to be encrypted

    Returns:
        bytes: The encrypted output
    """
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
