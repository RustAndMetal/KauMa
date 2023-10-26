from typing import List


def turn_rotors(rotors: List[List[int]], turn_list: List[List[int]]) -> None:
    """Turns the rotors

    Args:
        rotors (List[List[int]]): A list of lists representing the rotors to be used for encryption
        turn_list (List[List[int]]): A list of lists of integers representing the current turn of the rotors
    """
    for index, rotor in enumerate(rotors):
        turn_list[index] += 1
        turn_list[index] %= len(rotor)
        if rotor[turn_list[index] - 1] != 0:
            break

def rotors_encrypt(rotors: List[List[int]], reverse_rotors: List[List[int]], turn_list: List[int], input: int) -> int:
    """Encrypts the input with the given rotors

    Args:
        rotors (List[List[int]]): A list of lists representing the rotors to be used for encryption
        reverse_rotors (List[List[int]]): A list of lists representing the reverse rotors to be used for encryption
        turn_list (List[int]): A list of integers representing the current turn of the rotors
        input (int): The input to be encrypted

    Returns:
        int: The encrypted output
    """
    for rotor, turn in zip(rotors, turn_list):
        input = rotor[(input + turn) % len(rotor)]
    input = input ^ 0xff
    for rotor, turn in zip(reverse_rotors, turn_list[::-1]):
        input = (rotor[input] - turn) % len(rotor)
    return input

def rotor_reverse_init(rotors: List[List[int]]) -> List[List[int]]:
    """Initializes the reverse rotors

    Args:
        rotors (List[List[int]]): A list of lists representing the rotors to be used for encryption, that need to be reversed

    Returns:
        List[List[int]]: A list of lists representing the reverse rotors
    """
    output: List[List[int]] = []
    for rotor in rotors[::-1]:
        current_output: List[int] = [0] * len(rotor)
        for index, value in enumerate(rotor):
            current_output[value] = index
        output.append(current_output)
    return output
