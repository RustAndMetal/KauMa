import traceback
import sys

from actions import decode_json, encode_json
from bytenigma import bytenigma
from logging import eprint

# argument parsing in main?
def main():
    if len(sys.argv) != 2:
        eprint("Usage: python3 main.py <input.json>")
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