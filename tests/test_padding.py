import base64
import socketserver
import pytest
import threading

from krypto import padding
from krypto.logging import eprint


@pytest.fixture
def setup_and_teardown_for_stuff():
    print("\nsetting up")
    host, port = "localhost", 9999
    with socketserver.TCPServer((host, port), padding.server.MyPaddingHandler) as server:
        print("Listening on {}:{}".format(host, port))
        threading.Thread(target=server.serve_forever, args=(), daemon=False).start()
        yield True
        print("\ntearing down")
        server.shutdown()
# TODO: write test generator for json files
def test_padding_oracle_attack(setup_and_teardown_for_stuff):
    iv = "f93fe3d2a87863f032cdf01a63b30046"
    ciphertext = "872e841d05f0dc8a2aa5b29785aae4da"
    rec = padding.client.recover("localhost", 9999, bytes.fromhex(iv), bytes.fromhex(ciphertext))
    assert rec == b"heeeeeeeeeeeeee\x01"
