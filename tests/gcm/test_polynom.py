import base64

from krypto.gcm import polynom


def test_polynomial_conversion():
    null_block = b"\x00" * 16
    null_exponents = []
    assert polynom.Polynom.from_block(null_block) == polynom.Polynom.from_exponents(null_exponents)
    
    short_block = base64.b64decode("CIGBAAAgAAAAAAAAAAAAAA==")
    short_exponents = [ 4, 8, 15, 16, 23, 42 ]
    assert polynom.Polynom.from_block(short_block) == polynom.Polynom.from_exponents(short_exponents)

    long_block = base64.b64decode("OkfFRfHYf/t/PILSC706Qg==")
    long_exponents = [2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 21, 23, 25, 29, 31, 32, 33,
                 34, 35, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 
                 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 74, 75,
                 76, 77, 80, 86, 88, 89, 91, 94, 100, 102, 103, 104, 106, 107,
                 108, 109, 111, 114, 115, 116, 118, 121, 126]
    assert polynom.Polynom.from_block(long_block) == polynom.Polynom.from_exponents(long_exponents)
    
def test_polynomial_arithmetic():
    assert polynom.Polynom(0) + polynom.Polynom(0) == polynom.Polynom(0)
    assert polynom.Polynom(0) + polynom.Polynom(0xdeadbeef) == polynom.Polynom(0xdeadbeef)
    assert polynom.Polynom(0xdeadbeef) + polynom.Polynom(0xcafeaffe) == polynom.Polynom(0x14531111)

    a = polynom.Polynom.from_block(base64.b64decode("jjYoD6kfN+/Y/g4Hl991Cw=="))
    b = polynom.Polynom.from_block(base64.b64decode("tQsToM4bzOQtot/1w4x8PA=="))
    assert a * b == polynom.Polynom.from_block(base64.b64decode("khnvYitpTW8Sv3ZUmFqasw=="))
