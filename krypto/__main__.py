import traceback
import sys

from krypto import bytenigma
from krypto.actions import decode_json, encode_json
from krypto.logging import eprint

def main():
    """The main-Function parses the input, calls the action and encodes the output
       It also handles errors and prints them to stderr
    """
    if len(sys.argv) != 2:
        eprint("Usage: python3 -m krypto <input.json>")
        return
    try:
        with open(sys.argv[1], "r") as f:
            action, data = decode_json(f)
        print(encode_json(action(**data)))
    except Exception as e:
        eprint(traceback.format_exc())
        eprint(e)
        return 

if __name__ == "__main__":
    main()