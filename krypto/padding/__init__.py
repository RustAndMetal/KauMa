import base64
from krypto.actions import action
from .client import recover
from . import server


@action("padding-oracle-attack")
def padding_oracle_attack(hostname: str, port: int, iv: str, ciphertext: str) -> dict:
    """parses and seerializes the input and output of the padding oracle attack

    Returns:
        dict: dictionary containing the plaintext in base64
    """
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    assert (
        len(ciphertext) % len(iv) == 0
    ), "Ciphertext must be a multiple of the block size"

    ciphertext_blocks = []
    for i in range(0, len(ciphertext), len(iv)):
        ciphertext_blocks.append(ciphertext[i : i + len(iv)])

    plaintext = b""
    for prev, block in zip([iv] + ciphertext_blocks, ciphertext_blocks):
        plaintext += recover(hostname, port, prev, block)
    return {"plaintext": base64.b64encode(plaintext).decode()}
