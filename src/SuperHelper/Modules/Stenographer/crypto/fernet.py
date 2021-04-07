# Builtin modules
from base64 import urlsafe_b64encode

# Non-builtin modules
from cryptography.fernet import Fernet, InvalidToken

_InvalidToken = InvalidToken


def build_fernet(key: bytes) -> Fernet:
    """Build a Fernet object to encrypt or decrypt data from the key.

    ### Positional arguments

    - key (bytes)
        - A derived key (can be derived using the KDF from make_kd())

    ### Returns

    A Fernet object

    ### Raises

    - TypeError
        - Raised when the parameters given are in incorrect types
    """
    # Type checking
    if not isinstance(key, bytes):
        raise TypeError(f"The key must be in bytes (given {type(key)})")

    # Initialise and return a Fernet object
    # Key will be Base64-encoded first
    return Fernet(urlsafe_b64encode(key))
