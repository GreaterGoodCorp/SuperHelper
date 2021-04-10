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


class Cryptographer:
    def __init__(self, salt: bytes, auth_key: bytes, encrypt: bool = True):
        self.salt = salt
        self.kdf = self.make_kdf(self.salt)
        self.auth_hash = str(hashlib.sha256(auth_key))
        self.key = self.kdf.derive(self.auth_hash.encode())
        self.is_encrypt = encrypt

    def encrypt(self, raw_data: bytes) -> bytes:
        if not self.is_encrypt:
            raise ValueError("Not an encrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        return fernet.encrypt(raw_data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        if self.is_encrypt:
            raise ValueError("Not a decrypter!")
        fernet = Cryptographer.make_fernet(self.key)
        try:
            return fernet.decrypt(encrypted_data)
        except InvalidToken:
            logger.exception("Invalid key")
            raise

    @staticmethod
    def make_encrypter(key: str) -> Cryptographer:
        return Cryptographer(Cryptographer.make_salt(), key.encode(), True)

    @staticmethod
    def make_decrypter(salt: str, key: str) -> Cryptographer:
        return Cryptographer(Cryptographer.decode_salt(salt), key.encode(), False)

    @staticmethod
    def make_salt() -> bytes:
        return os.urandom(16)

    @staticmethod
    def encode_salt(salt: bytes) -> str:
        return str(base64.b64encode(salt), "utf-8")

    @staticmethod
    def decode_salt(salt: str) -> bytes:
        return base64.b64decode(bytes(salt, "utf-8"))

    @staticmethod
    def make_kdf(salt: bytes) -> PBKDF2HMAC:
        return PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend(),
        )

    @staticmethod
    def make_fernet(key: bytes) -> Fernet:
        return Fernet(base64.urlsafe_b64encode(key))


__all__ = ["Cryptographer"]
