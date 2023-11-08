import base64
from krypto.actions import action
from .client import recover

@action("padding-oracle-attack")
def padding_oracle_attack(hostname: str, port: int, iv: str, ciphertext: str) -> dict:
    """parses and seerializes the input and output of the padding oracle attack

    Returns:
        dict: dictionary containing the plaintext in base64
    """
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    plaintext = recover(hostname, port, iv, ciphertext)
    return {
        "plaintext": base64.b64encode(plaintext).decode()
    }