def recover(host: str, port: int, iv: bytes, ciphertext: bytes) -> bytes:
    """Recovers the plaintext from the server.

    Args:
        host (str): hostname of the padding-oracle-server
        port (int): port to connect to
        iv (bytes): iv used for encryption
        ciphertext (bytes): one block ciphertext
    
    Returns:
        bytes: plaintext
    """
    return b""
