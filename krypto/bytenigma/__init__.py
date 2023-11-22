import base64
from typing import List
from krypto.actions import action
from .rotors import rotors_encrypt, rotor_reverse_init, turn_rotors


@action("bytenigma")
def bytenigma(rotors: List[List[int]], input: str) -> dict:
    """Encrypts the input with the given rotors

    Args:
        rotors (List[List[int]]): A list of lists representing the rotors to be used for encryption
        input (str): The input to be encrypted in base64

    Returns:
        dict: dictionary containg the encrypted output in base64
    """
    inp = base64.b64decode(input)
    # init reverse rotors
    reverse_rotors = rotor_reverse_init(rotors)
    final_output = []
    turn_list: List[int] = [0] * len(rotors)
    # send input(single byte) through rotors
    for byte in inp:
        # returns one encrypted byte int
        output = rotors_encrypt(rotors, reverse_rotors, turn_list, byte)
        # append output to output list
        final_output.append(output)
        # turn rotors
        turn_rotors(rotors, turn_list)

    return {"output": base64.b64encode(bytes(final_output)).decode()}
