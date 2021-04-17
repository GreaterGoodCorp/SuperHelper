# This module defines the Cryptographer class, a utility class for cryptographic functions.
from __future__ import annotations

import base64
import os
import hashlib
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)

__all__ = [
    "Cryptographer",
]


class Cryptographer:
    """
    A utility class for cryptographic functions.
    """
    def __init__(self, salt: bytes, auth_key: bytes, encrypt: bool = True) -> None:
        self.salt = salt
        self.kdf = self.make_kdf(self.salt)
        self.auth_hash = hashlib.sha256(auth_key).digest()
        self.key = self.kdf.derive(self.auth_hash)
        self.is_encrypt = encrypt

    def encrypt(self, raw_data: bytes) -> bytes:
        """Encrypts raw data.

        :param raw_data: The raw data to be encrypted
        :type raw_data: bytes
        :return: The encrypted data
        :rtype: bytes
        """
        if not self.is_encrypt:
            raise ValueError("Not an encrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        return fernet.encrypt(raw_data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypts encrypted data.

        :param encrypted_data: The encrypted data to be decrypted
        :type encrypted_data: bytes
        :return: The decrypted data
        :rtype: bytes
        """
        if self.is_encrypt:
            raise ValueError("Not a decrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        try:
            return fernet.decrypt(encrypted_data)
        except InvalidToken:
            raise

    def get_salt_string(self) -> str:
        """String-ify the raw salt.

        :return: The Base64-encoded string of the raw salt
        :rtype: str
        """
        return Cryptographer.encode_salt(self.salt)

    @staticmethod
    def make_encrypter(salt: str, key: str) -> Cryptographer:
        """Makes a Fernet encrypter for salt and key.

        :param salt: The Base64-encoded string of the raw salt
        :type salt: str
        :param key: The authentication key
        :type key: str
        :return: A Cryptographer encrypter
        :rtype: Cryptographer
        """
        return Cryptographer(Cryptographer.decode_salt(salt), key.encode(), True)

    @staticmethod
    def make_decrypter(salt: str, key: str) -> Cryptographer:
        """Makes a Fernet decrypter for salt and key.

        :param salt: The Base64-encoded string of the raw salt
        :type salt: str
        :param key: The authentication key
        :type key: str
        :return: A Cryptographer decrypter
        :rtype: Cryptographer
        """
        return Cryptographer(Cryptographer.decode_salt(salt), key.encode(), False)

    @staticmethod
    def make_salt() -> bytes:
        """Generates a cryptographically secure salt for cryptography.

        :return: A 16-byte raw salt
        :rtype: bytes
        """
        return os.urandom(16)

    @staticmethod
    def encode_salt(salt: bytes) -> str:
        """Encodes the raw salt as string.

        :param salt: The raw salt
        :type salt: bytes
        :return: The Base64-encoded string of the raw salt
        :rtype: str
        """
        return str(base64.b64encode(salt), "utf-8")

    @staticmethod
    def decode_salt(salt: str) -> bytes:
        """Decodes the salt string to raw salt.

        :param salt: The Base64-encoded string of the raw salt
        :type salt: str
        :return: The raw salt
        :rtype: bytes
        """
        return base64.b64decode(bytes(salt, "utf-8"))

    @staticmethod
    def make_kdf(salt: bytes) -> PBKDF2HMAC:
        """Makes a key derivation function from raw salt.

        :param salt: The raw salt
        :type salt: bytes
        :return: A PBKDF2HMAC instance
        :rtype: PBKDF2HMAC
        """
        return PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend(),
        )

    @staticmethod
    def make_fernet(key: bytes) -> Fernet:
        """Makes a Fernet encrypter/decrypter from the derived key.

        :param key: The derived key
        :type key: bytes
        :return: A Fernet instance
        :rtype: Fernet
        """
        return Fernet(base64.urlsafe_b64encode(key))
