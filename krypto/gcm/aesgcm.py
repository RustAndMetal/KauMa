from . import polynom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESGCM:
    """Class to encrypt plaintext with AES GCM"""

    def __init__(
        self, key: bytes, nonce: bytes, associated_data: bytes, plaintext: bytes
    ):
        assert len(key) == 16, "Key must be 16 bytes long"
        self.key = key

        assert len(nonce) == 12, "Nonce must be 12 bytes long"
        self.nonce = nonce

        self.associated_data = associated_data

        self.plaintext = plaintext

        self.encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()

    def create_auth_key(self) -> bytes:
        """Function to create auth key

        Returns:
            bytes: auth key
        """
        null_block = b"\x00" * 16
        encryptor = Cipher(algorithms.AES(self.key), modes.ECB()).encryptor()
        return encryptor.update(null_block) + encryptor.finalize()

    def encrypt_block(self, block: bytes, counter: int) -> bytes:
        """encrypts plaintext with generated y block

        Args:
            y (int): counter int
            block (bytes): plaintext block

        Returns:
            bytes: encrypted block
        """
        return bytes(
            a ^ b for a, b in zip(block, self.generate_encrypted_counter(counter))
        )

    def generate_encrypted_counter(self, counter: int) -> bytes:
        # TODO maybe generator pattern machen
        """function to generate encrypted counter block

        Args:
            counter (int): current Counter

        Returns:                                                            x
            y (bytes): encrypted counter block
        """
        y = self.generate_counter(counter)
        encryptor = Cipher(algorithms.AES(self.key), modes.ECB()).encryptor()
        return encryptor.update(y) + encryptor.finalize()

    def generate_counter(self, counter: int) -> bytes:
        # TODO maybe generator pattern machen
        """function to generate counter block

        Args:
            counter (int): current Counter

        Returns:
            y (bytes): counter block
        """
        y = self.nonce + counter.to_bytes(length=4, byteorder="big")
        return y

    def gen_ciphertext(self) -> bytes:
        """function to generate ciphertext

        Returns:
            bytes: ciphertext
        """
        ciphertext = b""
        for i in range(-(len(self.plaintext) // -16)):
            ciphertext += self.encrypt_block(
                self.plaintext[i * 16 : (i + 1) * 16], i + 2
            )
        return ciphertext

    def ghash(self, ciphertext: bytes) -> bytes:
        """function to generate ghash

        Args:
            ciphertext (bytes): ciphertext
        """
        adder = polynom.Polynom(0)
        auth_key = polynom.Polynom.from_block(self.create_auth_key())
        for i in range(-(len(self.associated_data) // -16)):
            block = self.associated_data[i * 16 : (i + 1) * 16]
            if len(block) < 16:
                block += b"\x00" * (16 - len(block))
            adder += polynom.Polynom.from_block(block)
            adder *= auth_key
        for i in range(-(len(ciphertext) // -16)):
            block = ciphertext[i * 16 : (i + 1) * 16]
            if len(block) < 16:
                block += b"\x00" * (16 - len(block))
            adder += polynom.Polynom.from_block(block)
            adder *= auth_key
        l = (len(self.associated_data) * 8).to_bytes(length=8, byteorder="big") + (
            len(ciphertext) * 8
        ).to_bytes(length=8, byteorder="big")
        adder += polynom.Polynom.from_block(l)
        adder *= auth_key
        return adder.to_block()

    def gen_auth_tag(self, ciphertext: bytes) -> bytes:
        """encrypts plaintext with given key, nonce and associated data
        Args:
            ciphertext(bytes): the ciphertext

        Returns:
            bytes: auth tag
        """
        auth_tag = polynom.Polynom.from_block(
            self.generate_encrypted_counter(1)
        ) + polynom.Polynom.from_block(self.ghash(ciphertext))
        return auth_tag.to_block()
