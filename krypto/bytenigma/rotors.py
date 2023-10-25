from typing import List


def turn_rotors(rotors: List[List[int]], turn_list: List[List[int]]) -> None:
    for index, rotor in enumerate(rotors):
        turn_list[index] += 1
        if rotor[turn_list[index] - 1] != 0:
            break

def rotors_encrypt(rotors: List[List[int]], reverse_rotors: List[List[int]], turn_list: List[int], input: int) -> int:
    for rotor, turn in zip(rotors, turn_list):
        input = rotor[(input + turn) % len(rotor)]
    input = input ^ 0xff
    for rotor, turn in zip(reverse_rotors, turn_list[::-1]):
        input = (rotor[input] - turn) % len(rotor)
    return input

def rotor_reverse_init(rotors: List[List[int]]) -> List[List[int]]:
    output: List[List[int]] = []
    for rotor in rotors[::-1]:
        current_output: List[int] = [0] * len(rotor)
        for index, value in enumerate(rotor):
            current_output[value] = index
        output.append(current_output)
    return output
