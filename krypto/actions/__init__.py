import base64
import json

from typing import Callable, Tuple

#global but private
__ACTIONS = {}

def decode_json(json_string: str) -> Tuple[Callable, dict]:
    """
    Decodes the JSON string and returns the action and input

    Args:
        json_string (str): The JSON string to decode
    
    Returns:
        tuple: A tuple containing the action and input
    """
    json_data = json.load(json_string)

    if "action" not in json_data:
        raise KeyError("No action in json specified")

    action = json_data["action"]

    if action not in __ACTIONS:
        raise KeyError("Unknown action: " + action)
    
    del json_data["action"]

    return __ACTIONS[action], json_data

def encode_json(output: dict) -> str:
    """
    Encodes the output dict to a JSON string

    Args:
        output (dict): The output dict to encode
    
    Returns:
        str: The JSON encoded output
    """
    return json.dumps(output)

def action(action_name):
    """
    Decorator for actions

    Args:
        action_name (str): The name of the action
    """
    def wrapper(f):
        __ACTIONS[action_name] = f
        return f
    return wrapper

