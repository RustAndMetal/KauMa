from krypto.actions import action
import base64
from typing import List
from .polynom import Polynom


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

