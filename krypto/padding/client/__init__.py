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
            valid_candidates = validated_candidates(real_iv, known_decrypted_bytes, sock, padding_byte)
            known_decrypted_bytes = decrypt_bytes(valid_candidates, real_iv, known_decrypted_bytes, sock, padding_byte)
        # Close connection with server by sending length 0
        sock.sendall((0).to_bytes(length=2, byteorder="little"))
    return bytes([a ^ b for a,b in zip(known_decrypted_bytes, real_iv)])

def validated_candidates(real_iv: bytes, known_decrypted_bytes: list, sock: socket.socket, padding_byte: int) -> list:
    """Validates the candidates for the padding byte

    Args:
        real_iv (bytes): iv used for encryption
        known_decrypted_bytes (list): list for the known decrypted bytes
        sock (socket.socket): socket to connect to the server
        padding_byte (int): padding byte to use for validatation

    Returns:
        list: list of valid candidates
    """
    valid_candidates = []
    sock.sendall((256).to_bytes(length=2, byteorder="little"))
    for candidate in range(256):
        iv = (
            [0] * (len(real_iv) - len(known_decrypted_bytes) - 1)
            + [candidate]
            + [padding_byte ^ b for b in known_decrypted_bytes]
        )
        assert len(iv) == len(real_iv)
        sock.sendall(bytes(iv))
    for candidate in range(256):
        if sock.recv(1) == b"\x01":
            valid_candidates.append(candidate)
    return valid_candidates

def decrypt_bytes(valid_candidates: list, real_iv: bytes, known_decrypted_bytes: list, sock: socket.socket, padding_byte: int) -> list:
    """Decrypts the bytes

    Args:
        valid_candidates (list): list of candidates that cause padding_byte to appear at the targeted index
        real_iv (bytes): iv used for encryption
        known_decrypted_bytes (list): list of the known decrypted bytes
        sock (socket.socket): socket to connect to the server
        padding_byte (int): padding byte to validate

    Returns:
        list: list of the known decrypted bytes, including the newly decrypted byte
    """
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
        # We mutate the list in the loop, so copy it
        # Otherwise, we would iterate over the list we are mutating
        # which would potentially not consume all bytes from the server.
        # Subsequent calls to sock.recv(1) would then return unexpected values.
        for candidate in list(valid_candidates):
            if sock.recv(1) == b"\x00":
                valid_candidates.remove(candidate)
    assert len(valid_candidates) == 1, "More than one valid candidate for padding byte"
    known_decrypted_bytes.insert(0, valid_candidates[0] ^ padding_byte)
    return known_decrypted_bytes
