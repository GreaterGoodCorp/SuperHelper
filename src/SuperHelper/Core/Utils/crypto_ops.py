# This module defines the Cryptographer class, a utility class for cryptographic functions.
from __future__ import annotations

import base64
import os
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

from SuperHelper.Core.Utils import TypeCheck

__all__ = [
    "Cryptographer",
]


class Cryptographer:
    """A utility class for cryptographic functions."""

    def __init__(self, salt: bytes, auth_key: bytes, encrypt: bool = True) -> None:
        """Initialises a `Cryptographer` instance.
        Args:
            salt (bytes): The raw salt, in bytes.
            auth_key (bytes): The authentication key, in bytes.
            encrypt (bool): True to make an encrypter, otherwise False.
        """
        self.salt = salt
        self.kdf = self.make_kdf(self.salt)
        self.auth_hash = hashlib.sha256(auth_key).digest()
        self.key = self.kdf.derive(self.auth_hash)
        self.is_encrypt = encrypt

    def encrypt(self, raw_data: bytes) -> bytes:
        """Encrypts raw data.

        Args:
            raw_data (bytes): The raw data to be encrypted.

        Returns:
            The encrypted data, in bytes, which is encrypted using the `Fernet` (created by `Cryptography.make_fernet`)

        Raises:
            ValueError: A decrypter is used to encrypt.
        """
        TypeCheck.ensure_bytes(raw_data, "raw_data")
        if not self.is_encrypt:
            raise ValueError("Not an encrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        return fernet.encrypt(raw_data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypts the encrypted data.

        Args:
            encrypted_data (bytes): The encrypted data to be decrypted.

        Returns:
            The decrypted data, in bytes, which is decrypted using the `Fernet` (created by `Cryptography.make_fernet`)
        """
        TypeCheck.ensure_bytes(encrypted_data, "encrypted_data")
        if self.is_encrypt:
            raise ValueError("Not a decrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        try:
            return fernet.decrypt(encrypted_data)
        except InvalidToken:
            raise

    def get_salt_string(self) -> str:
        """String-ify the raw salt.

        Returns:
            The Base64-encoded string of the raw salt.
        """
        return Cryptographer.encode_salt(self.salt)

    @staticmethod
    def make_encrypter(salt: str, key: str) -> Cryptographer:
        """Makes a Fernet encrypter for salt and key.

        Args:
            salt (str): The Base64-encoded string of the raw salt.
            key (str): The authentication key.

        Returns:
            A `Cryptographer` instance, which can be used to encrypt data.
        """
        TypeCheck.ensure_str(salt, "salt")
        TypeCheck.ensure_str(key, "key")
        return Cryptographer(Cryptographer.decode_salt(salt), key.encode(), True)

    @staticmethod
    def make_decrypter(salt: str, key: str) -> Cryptographer:
        """Makes a Fernet decrypter for salt and key.

        Args:
            salt (str): The Base64-encoded string of the raw salt.
            key (str): The authentication key.

        Returns:
            A `Cryptographer` instance, which can be used to decrypt data.
        """
        TypeCheck.ensure_str(salt, "salt")
        TypeCheck.ensure_str(key, "key")
        return Cryptographer(Cryptographer.decode_salt(salt), key.encode(), False)

    @staticmethod
    def make_salt() -> bytes:
        """Generates a cryptographically secure salt for cryptography.

        Returns:
            A 16-byte raw salt
        """
        return os.urandom(16)

    @staticmethod
    def encode_salt(salt: bytes) -> str:
        """Encodes the raw salt as string.

        Args:
            salt (bytes): The raw salt, in bytes.

        Returns:
            The Base64-encoded string of the raw salt
        """
        TypeCheck.ensure_bytes(salt, "salt")
        return str(base64.b64encode(salt), "utf-8")

    @staticmethod
    def decode_salt(salt: str) -> bytes:
        """Decodes the salt string to raw salt.

        Args:
            salt (str): The Base64-encoded string of the raw salt.

        Returns:
            The raw salt
        """
        TypeCheck.ensure_str(salt, "salt")
        return base64.b64decode(bytes(salt, "utf-8"))

    @staticmethod
    def make_kdf(salt: bytes) -> PBKDF2HMAC:
        """Makes a key derivation function from raw salt.

        Args:
            salt (bytes): The raw salt, in bytes.

        Returns:
            A PBKDF2HMAC instance, which can be used to derive key from the authentication key.
        """
        TypeCheck.ensure_bytes(salt, "salt")
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

        Args:
            key (bytes): The derived key, in bytes.

        Returns:
            A Fernet instance, which can be used to either encrypt or decrypt data.
        """
        TypeCheck.ensure_bytes(key, "key")
        return Fernet(base64.urlsafe_b64encode(key))
