from . import polynom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESGCM:
    """Class to encrypt plaintext with AES GCM"""

    def __init__(
        self, key: bytes, nonce: bytes, associated_data: bytes, plaintext: bytes
    ):
        self._associated_data = associated_data
        """bytes: associated data of any length"""

        self._plaintext = plaintext
        """bytes: plaintext of any length"""

        self._keystream_generator = self._get_keystream_generator(key, nonce)
        """bytes: keystream generator object, yields encrypted counter blocks"""

        self._auth_tag_mask = next(self._keystream_generator)
        """bytes: auth tag mask, first encrypted counter block"""

        self._auth_key = self._encrypt(key, b"\x00" * 16)
        """bytes: auth key, encrypted Null block"""

        self._y0 = nonce + (1).to_bytes(length=4, byteorder="big")
        """only used for testing, not needed for encryption"""

    @property
    def auth_key(self) -> bytes:
        """property to get auth key

        Returns:
            bytes: auth key
        """
        return self._auth_key

    @property
    def y0(self) -> bytes:
        """property to get y0

        Returns:
            bytes: y0
        """
        return self._y0

    def _encrypt(self, key: bytes, block: bytes) -> bytes:
        """encrypts block with given key

        Args:
            key (bytes): key
            block (bytes): block to encrypt

        Returns:
            bytes: encrypted block
        """
        assert len(block) == 16, "Block must be 16 bytes long"
        assert len(key) == 16, "Key must be 16 bytes long"
        encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
        return encryptor.update(block) + encryptor.finalize()

    def _get_keystream_generator(self, key: bytes, nonce: bytes) -> bytes:
        """function for returning keystream generator object

        Args:
            key (bytes): key
            nonce (bytes): nonce

        Returns:
            bytes: keystream generator object
        """
        counter = 0
        while True:
            counter += 1
            y = nonce + counter.to_bytes(length=4, byteorder="big")
            yield self._encrypt(key, y)

    def encrypt_block(self, block: bytes) -> bytes:
        """encrypts plaintext with generated y block

        Args:
            y (int): counter int
            block (bytes): plaintext block

        Returns:
            bytes: encrypted block
        """
        return bytes(a ^ b for a, b in zip(block, next(self._keystream_generator)))

    def gen_ciphertext(self) -> bytes:
        """function to generate ciphertext

        Returns:
            bytes: ciphertext
        """
        ciphertext = b""
        for i in range(-(len(self._plaintext) // -16)):
            ciphertext += self.encrypt_block(self._plaintext[i * 16 : (i + 1) * 16])
        return ciphertext

    def ghash(self, ciphertext: bytes) -> bytes:
        """function to generate ghash

        Args:
            ciphertext (bytes): ciphertext

        Returns:
            bytes: ghash
        """
        adder = polynom.Polynom(0)
        auth_key = polynom.Polynom.from_block(self._auth_key)
        for input_list in [self._associated_data, ciphertext]:
            for i in range(-(len(input_list) // -16)):
                block = input_list[i * 16 : (i + 1) * 16]
                if len(block) < 16:
                    block += b"\x00" * (16 - len(block))
                adder += polynom.Polynom.from_block(block)
                adder *= auth_key
        l = (len(self._associated_data) * 8).to_bytes(length=8, byteorder="big") + (
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
            self._auth_tag_mask
        ) + polynom.Polynom.from_block(self.ghash(ciphertext))
        return auth_tag.to_block()
