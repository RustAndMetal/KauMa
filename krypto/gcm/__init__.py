from krypto.actions import action
import base64
from typing import List
from .polynom import Polynom
from .aesgcm import AESGCM
from .meta_polynom import MetaPolynom
from .cantor import gcm_recover


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
    gcm = AESGCM(
        base64.b64decode(key),
        base64.b64decode(nonce),
        base64.b64decode(associated_data),
        base64.b64decode(plaintext),
    )
    ciphertext = gcm.gen_ciphertext()
    auth_tag = gcm.gen_auth_tag(ciphertext)
    Y0 = gcm.y0
    H = gcm.auth_key
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "auth_tag": base64.b64encode(auth_tag).decode(),
        "Y0": base64.b64encode(Y0).decode(),
        "H": base64.b64encode(H).decode(),
    }


def base64_to_MetaPolynom(a: List[str]) -> MetaPolynom:
    """Converts a list of base64 encoded polynomials to a MetaPolynom

    Args:
        a (List[str]): The list of base64 encoded polynomials

    Returns:
        MetaPolynom: The MetaPolynom
    """
    a = [polynom.Polynom.from_block(base64.b64decode(x)) for x in a]
    return MetaPolynom(a)


def MetaPolynom_to_base64(a: MetaPolynom) -> List[str]:
    """Converts a MetaPolynom to a list of base64 encoded polynomials

    Args:
        a (MetaPolynom): The MetaPolynom

    Returns:
        List[str]: The list of base64 encoded polynomials
    """
    return [base64.b64encode(x.to_block()).decode() for x in a]


def gcm_poly_arithmetic_action(f):
    def action(a: List[str], b: List[str]) -> dict:
        """Performs an arithmetic operation on two polynomials

        Args:
            a (List[str]): The first polynomial
            b (List[str]): The second polynomial

        Returns:
            dict: dictionary containing the result
        """
        result = f(base64_to_MetaPolynom(a), base64_to_MetaPolynom(b))
        return {"result": MetaPolynom_to_base64(result)}

    return action


action("gcm-poly-add")(gcm_poly_arithmetic_action(lambda a, b: a + b))
action("gcm-poly-mul")(gcm_poly_arithmetic_action(lambda a, b: a * b))
action("gcm-poly-div")(gcm_poly_arithmetic_action(lambda a, b: a // b))
action("gcm-poly-mod")(gcm_poly_arithmetic_action(lambda a, b: a % b))
action("gcm-poly-gcd")(gcm_poly_arithmetic_action(lambda a, b: a.gcd(b)))


@action("gcm-poly-pow")
def gcm_poly_pow(base: List[str], exponent: int) -> dict:
    """Calculates the power of a polynomial

    Args:
        base (List[str]): The polynomial base
        exponent (int): The exponent

    Returns:
        dict: dictionary containing the power of the polynomial
    """
    result = base64_to_MetaPolynom(base) ** exponent
    return {"result": MetaPolynom_to_base64(result)}


@action("gcm-poly-powmod")
def gcm_poly_powmod(base: List[str], exponent: int, modulo: List[str]) -> dict:
    """Calculates the power of a polynomial modulo another polynomial

    Args:
        base (List[str]): The polynomial base
        exponent (int): The exponent
        modulo (List[str]): The modulo

    Returns:
        dict: dictionary containing the power of the polynomial modulo another polynomial
    """
    result = pow(base64_to_MetaPolynom(base), exponent, base64_to_MetaPolynom(modulo))
    return {"result": MetaPolynom_to_base64(result)}


@action("gcm-recover")
def gcm_recover(nonce: str, msg1: dict, msg2: dict, msg3: dict, msg4: dict) -> dict:
    """Recovers the auth_tag of a message encrypted with GCM

    Args:
        nonce (str): The nonce (unused, maybe use later to check that every message used the same one)
        msg1 (dict): The first message
        msg2 (dict): The second message
        msg3 (dict): The third message
        msg4 (dict): The fourth message without auth_tag

    Returns:
        dict: dictionary containing the recovered plaintext
    """

    def base64_msg_decode(msg):
        result = {
            "ciphertext": base64.b64decode(msg["ciphertext"]),
            "associated_data": base64.b64decode(msg["associated_data"]),
        }
        if "auth_tag" in msg:
            result["auth_tag"] = base64.b64decode(msg["auth_tag"])
        return result

    msg1 = base64_msg_decode(msg1)
    msg2 = base64_msg_decode(msg2)
    msg3 = base64_msg_decode(msg3)
    msg4 = base64_msg_decode(msg4)
    msg4_tag = cantor.gcm_recover(msg1, msg2, msg3, msg4)
    return {"msg4_tag": base64.b64encode(msg4_tag).decode()}
