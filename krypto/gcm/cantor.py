from . import meta_polynom
from . import polynom
from typing import Optional


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
