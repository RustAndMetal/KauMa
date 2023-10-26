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
    
    json_data["input"] = base64.b64decode(json_data["input"])

    action = json_data["action"]

    if action not in __ACTIONS:
        raise KeyError("Unknown action: " + action)
    
    del json_data["action"]

    return __ACTIONS[action], json_data

def encode_json(output: str) -> str:
    """
    Encodes the output string to JSON

    Args:
        output (str): The output string to encode
    
    Returns:
        str: The JSON encoded output
    """
    output = base64.b64encode(output).decode("utf-8")
    return json.dumps({"output": output})

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

