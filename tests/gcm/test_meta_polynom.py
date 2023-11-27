from krypto.gcm import base64_to_MetaPolynom, cantor


def test_cantor():
    f = [
        "7A9C3400001A584BB29B0A03B7971984",
        "1B81C000000000A9D95C170026D05960",
        "F43800000000000000C45E91CFDC121E",
        "000000000000000000000000DE6DF8F8",
        "80000000000000000000000000000000",
    ]
    f = base64_to_MetaPolynom(f)
    for i in range(100):
        x = cantor.cantor_zassenhaus(f, f)
        if x is not None:
            break
    assert x is not None
    assert (x[0] * x[1]).to_monic() == f.to_monic()
