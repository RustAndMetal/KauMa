import socketserver
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class MyPaddingHandler(socketserver.BaseRequestHandler):
    """Provide a handler for the padding oracle server."""
    CIPHER_LENGTH = 16
    KEY = bytes.fromhex("5aa12150f253545d6867b1bd40ed03bd4ae90921dec464372a2f77c68edf777f")

    def handle(self):
        ciphertext = self.receive_cipher()
        while (length := self.receive_length()) != 0:
            for _ in range(length):
                iv = self.receive_n_bytes(self.CIPHER_LENGTH)
                cipher = Cipher(algorithms.AES(self.KEY), modes.CBC(iv))
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                unpadder = padding.PKCS7(self.CIPHER_LENGTH * 8).unpadder()
                try:
                    unpadder.update(plaintext) + unpadder.finalize()
                    self.request.sendall(b"\x01")
                except ValueError:
                    self.request.sendall(b"\x00")

    def receive_cipher(self) -> bytes:
        """receives the cipher from the client

        Returns:
            bytes: the cipher
        """
        return self.receive_n_bytes(self.CIPHER_LENGTH)
    
    def receive_length(self) -> int:
        """receives a two byte little endian value from the client

        Returns:
            int: the length
        """
        return int.from_bytes(self.receive_n_bytes(2), "little")
    
    def receive_n_bytes(self, n: int) -> bytes:
        """receives exactly n bytes from the client

        Args:
            n (int): the number of bytes to receive

        Returns:
            bytes: the received bytes
        """
        out = b""
        while len(out) < n:
            out += self.request.recv(n - len(out))
        return out
