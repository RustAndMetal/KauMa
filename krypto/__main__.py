import importlib
import pkgutil
import traceback
import sys

# This is a workaround to import all submodules of krypto, so that actions are registered
import krypto
for finder, name, ispkg in pkgutil.iter_modules(krypto.__path__, krypto.__name__ + "."):
    if not name.endswith(".__main__"):
        importlib.import_module(name)

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