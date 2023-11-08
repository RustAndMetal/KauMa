import socket


def recover(host: str, port: int, real_iv: bytes, ciphertext: bytes) -> bytes:
    """Recovers the plaintext from the server.

    Args:
        host (str): hostname of the padding-oracle-server
        port (int): port to connect to
        real_iv (bytes): iv used for encryption
        ciphertext (bytes): one block ciphertext

    Returns:
        bytes: plaintext
    """
    with socket.create_connection((host, port)) as sock:
        sock.sendall(ciphertext)

        known_decrypted_bytes = []
        for i in reversed(range(len(real_iv))):
            padding_byte = len(real_iv) - i
            sock.sendall((256).to_bytes(length=2, byteorder="little"))
            for candidate in range(256):
                iv = (
                    [0] * (len(real_iv) - len(known_decrypted_bytes) - 1)
                    + [candidate]
                    + [padding_byte ^ b for b in known_decrypted_bytes]
                )
                assert len(iv) == len(real_iv)
                sock.sendall(bytes(iv))
            valid_candidates = []
            for candidate in range(256):
                if sock.recv(1) == b"\x01":
                    valid_candidates.append(candidate)
            if len(valid_candidates) > 1:
                assert padding_byte == 1, "Only for the first padding byte, two valid paddings can occur"
                sock.sendall(len(valid_candidates).to_bytes(length=2, byteorder="little"))
                for candidate in valid_candidates:
                    iv = (
                        [0xff] * (len(real_iv) - len(known_decrypted_bytes) - 1)
                        + [candidate]
                        + [padding_byte ^ b for b in known_decrypted_bytes]
                    )
                    sock.sendall(bytes(iv))
                for candidate in valid_candidates:
                    if sock.recv(1) == b"\x00":
                        valid_candidates.remove(candidate)
            assert len(valid_candidates) == 1, "More than one valid candidate for padding byte"
            known_decrypted_bytes.insert(0, valid_candidates[0] ^ padding_byte)

    return bytes([a ^ b for a,b in zip(known_decrypted_bytes, real_iv)])
