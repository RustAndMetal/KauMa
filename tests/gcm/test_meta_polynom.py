from krypto.gcm import base64_to_MetaPolynom, cantor
import base64


def test_cantor():
    f = [
        "epw0AAAaWEuymwoDt5cZhA==",
        "G4HAAAAAAKnZXBcAJtBZYA==",
        "9DgAAAAAAAAAxF6Rz9wSHg==",
        "AAAAAAAAAAAAAAAA3m34+A==",
        "gAAAAAAAAAAAAAAAAAAAAA==",
    ]
    f = base64_to_MetaPolynom(f)
    for i in range(100):
        x = cantor.cantor_zassenhaus(f, f)
        if x is not None:
            break
    assert x is not None
    assert (x[0] * x[1]).to_monic() == f.to_monic()


def test_zeros():
    # f = [
    #     b'z\x9c4\x00\x00\x1aXK\xb2\x9b\n\x03\xb7\x97\x19\x84',
    #     b'\x1b\x81\xc0\x00\x00\x00\x00\xa9\xd9\\\x17\x00&\xd0Y`',
    #     b'\xf48\x00\x00\x00\x00\x00\x00\x00\xc4^\x91\xcf\xdc\x12\x1e',
    #     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdem\xf8\xf8',
    #     b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # ]
    f = [
        "epw0AAAaWEuymwoDt5cZhA==",
        "G4HAAAAAAKnZXBcAJtBZYA==",
        "9DgAAAAAAAAAxF6Rz9wSHg==",
        "AAAAAAAAAAAAAAAA3m34+A==",
        "gAAAAAAAAAAAAAAAAAAAAA==",
    ]
    f = base64_to_MetaPolynom(f)
    p = [
        "AAAAAAAAAAAAAAAA3q2+7w==",
        "AAAAAAAAAAAAAAAAAACrzQ==",
        "AAAAAAAAAAAAAAAAAAASNA==",
        "AAAAAAAAAAAAAAAAAMD/7g==",
    ]
    zeros = cantor.find_zeros(f)
    zeros = [x.to_block() for x in zeros]
    zeros = [base64.b64encode(x).decode() for x in zeros]
    assert set(zeros) == set(p)
