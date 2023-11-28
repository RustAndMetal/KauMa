from . import meta_polynom, polynom, aesgcm
from typing import Optional, List


def cantor_zassenhaus(
    f: meta_polynom.MetaPolynom, p: meta_polynom.MetaPolynom
) -> Optional[tuple[meta_polynom.MetaPolynom, meta_polynom.MetaPolynom]]:
    """Calculates two factors of a polynomial with cantor zassenhaus algorithm

    Args:
        f (meta_polynom.MetaPolynom): factorization modulo
        p (meta_polynom.MetaPolynom): factorization polynom

    Returns:
        Optional[tuple[meta_polynom.MetaPolynom, meta_polynom.MetaPolynom]]: two factors of the polynomial
    """
    f = f.to_monic()
    p = p.to_monic()
    one = meta_polynom.MetaPolynom([polynom.Polynom(1)])

    q = 2**128

    h = meta_polynom.MetaPolynom.rand_poly(len(f) - 1)

    g = pow(h, ((q - 1) // 3), f) - one

    q = meta_polynom.MetaPolynom.gcd(p, g)

    if q != one and q != p:
        k1 = q
        k2 = p // q
        assert p == k1 * k2, "p != k1 * k2, cantor_zassenhaus failed"
        return (k1.to_monic(), k2.to_monic())
    else:
        return None


def find_zeros(f: meta_polynom.MetaPolynom) -> List[polynom.Polynom]:
    """Finds the zeros of a polynomial with cantor zassenhaus algorithm

    Args:
        f (meta_polynom.MetaPolynom): The polynomial

    Returns:
        List[polynom.Polynom]: The zeros of the polynomial
    """
    zeros: List[polynom.Polynom] = [f]
    while any([len(zero) > 2 for zero in zeros]):

        for zero in zeros:
            if len(zero) > 2:
                p = zero
                break
        result = cantor_zassenhaus(f, p)
        if result is not None:
            k1, k2 = result
            zeros.remove(p)
            zeros.append(k1)
            zeros.append(k2)
    return [zero[0] for zero in zeros]


def simple_ghash(
    auth_key: polynom.Polynom, ciphertext: bytes, associated_data: bytes
) -> polynom.Polynom:
    """Calculates a q block of GCM

    Args:
        auth_key (polynom.Polynom): auth_key from message
        ciphertext (bytes): message ciphertext
        associated_data (bytes): message associated_data

    Returns:
        polynom.Polynom: the q block as polynom
    """
    adder = polynom.Polynom(0)
    for input_list in [associated_data, ciphertext]:
        for i in range(-(len(input_list) // -16)):
            block = input_list[i * 16 : (i + 1) * 16]
            if len(block) < 16:
                block += b"\x00" * (16 - len(block))
            adder += polynom.Polynom.from_block(block)
            adder *= auth_key
    l = (len(associated_data) * 8).to_bytes(length=8, byteorder="big") + (
        len(ciphertext) * 8
    ).to_bytes(length=8, byteorder="big")
    adder += polynom.Polynom.from_block(l)
    adder *= auth_key
    return adder


def gcm_recover(msg1: dict, msg2: dict, msg3: dict, msg4: dict) -> bytes:
    """Recovers the auth tag of a GCM message

    Args:
        msg1 (dict): The first message
        msg2 (dict): The second message
        msg3 (dict): The third message
        msg4 (dict): The fourth message without auth_tag

    Returns:
        bytes: The recovered auth_tag
    """
    # TODO refactor to beauty, ghash generator
    qs = []
    for msg in [msg1, msg2]:
        q: List[polynom.Polynom] = []
        for input_list in [msg["associated_data"], msg["ciphertext"]]:
            for i in range(-(len(input_list) // -16)):
                block = input_list[i * 16 : (i + 1) * 16]
                if len(block) < 16:
                    block += b"\x00" * (16 - len(block))
                q.append(polynom.Polynom.from_block(block))
        l = (len(msg["associated_data"]) * 8).to_bytes(length=8, byteorder="big") + (
            len(msg["ciphertext"]) * 8
        ).to_bytes(length=8, byteorder="big")
        q.append(polynom.Polynom.from_block(l))
        qs.append(q)
    f_length = max(len(qs[0]), len(qs[1])) + 1
    f_coeffs = [polynom.Polynom(0)] * f_length
    for i in range(1, f_length):
        f_coeffs[i] += qs[0].pop() if len(qs[0]) > 0 else polynom.Polynom(0)
        f_coeffs[i] += qs[1].pop() if len(qs[1]) > 0 else polynom.Polynom(0)
    f_coeffs[0] = polynom.Polynom.from_block(
        msg1["auth_tag"]
    ) + polynom.Polynom.from_block(msg2["auth_tag"])
    f = meta_polynom.MetaPolynom(f_coeffs)
    h_candidates = find_zeros(f)
    assert len(h_candidates) > 0, "no h candidates found"
    for h in h_candidates:
        ek_y0 = simple_ghash(
            h, msg1["ciphertext"], msg1["associated_data"]
        ) + polynom.Polynom.from_block(msg1["auth_tag"])
        q_block = simple_ghash(h, msg3["ciphertext"], msg3["associated_data"])
        tag_msg3 = q_block + ek_y0
        if tag_msg3 == polynom.Polynom.from_block(msg3["auth_tag"]):
            q_block = simple_ghash(h, msg4["ciphertext"], msg4["associated_data"])
            tag_msg4 = q_block + ek_y0
            return tag_msg4.to_block()
    assert False, "no h candidates worked"
