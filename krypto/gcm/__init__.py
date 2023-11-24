from krypto.actions import action
import base64
from typing import List
from .polynom import Polynom
from .aesgcm import AESGCM


@action("gcm-block2poly")
def gcm_block2poly(block: str) -> dict:
    """Converts a block of GCM to a polynomial

    Args:
        block (str): The block to be converted

    Returns:
        dict: dictionary containing the polynomial exponents
    """
    inp = base64.b64decode(block)
    exponents = Polynom.from_block(inp).to_exponents()
    return {"exponents": exponents}


@action("gcm-poly2block")
def gcm_poly2block(exponents: List[int]) -> dict:
    """Converts a polynomial to a block of GCM

    Args:
        poly (str): The polynomial exponents to be converted

    Returns:
        dict: dictionary containing the block
    """
    block = Polynom.from_exponents(exponents).to_block()
    return {"block": base64.b64encode(block).decode()}


@action("gcm-clmul")
def gcm_clmul(a: str, b: str) -> dict:
    """Performs a carryless multiplication of two polynomials

    Args:
        a (str): The first polynomial
        b (str): The second polynomial

    Returns:
        dict: dictionary containing the result
    """
    a = polynom.Polynom.from_block(base64.b64decode(a))
    b = polynom.Polynom.from_block(base64.b64decode(b))
    result = (a * b).to_block()
    return {"a_times_b": base64.b64encode(result).decode()}

@action("gcm-encrypt")
def gcm_encrypt(key: str, nonce: str, associated_data: str, plaintext: str) -> dict:
    """Encrypts the plaintext with the given key, nonce and associated data

    Args:
        key (str): The key to be used for encryption
        nonce (str): The nonce to be used for encryption
        associated_data (str): The associated data to be used for encryption
        plaintext (str): The plaintext to be encrypted

    Returns:
        dict: dictionary containing the ciphertext, auth_tag, Y0 and H
    """
    gcm = aesgcm.AESGCM(
        base64.b64decode(key),
        base64.b64decode(nonce),
        base64.b64decode(associated_data),
        base64.b64decode(plaintext),
    )
    ciphertext = gcm.gen_ciphertext()
    auth_tag = gcm.gen_auth_tag(ciphertext)
    Y0 = gcm.generate_counter(1)
    H = gcm.create_auth_key()
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "auth_tag": base64.b64encode(auth_tag).decode(),
        "Y0": base64.b64encode(Y0).decode(),
        "H": base64.b64encode(H).decode(),
    }

