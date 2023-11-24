import base64
import pytest
from krypto.gcm import aesgcm


@pytest.fixture
def setup():
    key = base64.b64decode("/v/pkoZlcxxtao+UZzCDCA==")
    nonce = base64.b64decode("yv66vvrO263eyviI")
    associated_data = ""
    plaintext = base64.b64decode(
        "2TEyJfiEBuWlWQnFr/UmmoanqVMVNPfaLkwwPYoxinIcPAyVlWgJUy/PDiRJprUl"
    )

    return aesgcm.AESGCM(key, nonce, associated_data, plaintext)


def test_gen_ciphertext_gcm(setup):
    ciphertext = base64.b64decode(
        "QoMewiF3dCRLciG3hNDUnOOqIS8sAqTgNcF+IymsoS4h1RSyVGaTHH2PalqshKoF"
    )
    assert setup.gen_ciphertext() == ciphertext


def test_create_auth_key_gcm(setup):
    H = base64.b64decode("uDtTNwi/U10KpuUpgNU7eA==")
    assert setup.create_auth_key() == H


def test_generate_counter_gcm(setup):
    y0 = base64.b64decode("yv66vvrO263eyviIAAAAAQ==")
    assert setup.generate_counter(1) == y0


def test_generate_auth_tag_gcm(setup):
    auth_tag = base64.b64decode("UWigU6JGUYX2sZ7CZaToiw==")
    ciphertext = base64.b64decode(
        "QoMewiF3dCRLciG3hNDUnOOqIS8sAqTgNcF+IymsoS4h1RSyVGaTHH2PalqshKoF"
    )
    assert setup.gen_auth_tag(ciphertext) == auth_tag
