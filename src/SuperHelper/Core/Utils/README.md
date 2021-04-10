# Subpackage `SuperHelper.Core.Utils`

This subpackage contains utilities implemented exclusively for the core CLI. APIs designed in this subpackage are
intended for internal use only.

Core commands are also documented here.

## Package content

1. Module `command.py`: Contains the core commands.

2. Module `loader.py`: Contains the module loader function.

3. Module `logger.py`: Contains the core logger initialisation function.

4. Module `bit_ops.py`: Contains the implementation of bitwise operations `BitOps`.

5. Module `crypto_ops.py`: Contains the implementation of cryptographic functions `Cryptographer`.

## API documentation

### Class `TracebackInfoFilter(logging.Filter)`

This class inherits from `logging.Filter`. This filter allows traceback to get logged into the log file, while blocking
it from `sys.stderr`.

This class is intended for internal use only.

### Class `BitOps`

This class defines many static methods to work with bits.

#### Method documentation

1. Static method `is_bit_set(i: int, pos: int) -> bool`

   This method returns `True` if the bit at position `pos`-th (from the least significant bit, zero-indexed) of the
   integer `i` is set. Otherwise, returns `False`.

   *Parameters*:

   * *`i` - The integer to check*

   * *`pos` - Position of the bit*

2. Static method `set_bit(i: int, pos: int) -> int`

   This method sets the bit at position `pos`-th (from the least significant bit, zero-indexed) of the integer `i`.

   *Parameters*:

   * *`i` - The integer to check*

   * *`pos` - Position of the bit*

3. Static method `unset_bit(i: int, pos: int) -> int`

   This method unsets the bit at position `pos`-th (from the least significant bit, zero-indexed) of the integer `i`.

   *Parameters*:

   * *`i` - The integer to check*

   * *`pos` - Position of the bit*

### Class `Cryptographer`

This class provides many ready-to-use cryptographic functions.

#### Method documentation

1. Method `encrypt(self, raw_data: bytes) -> bytes`

   This method encrypts the `raw_data` with the authentication key provided during initialization.

   *Parameters*: *`raw_data` - The raw (binary) data*

2. Method `decrypt(self, encrypted_data: bytes) -> bytes`

   This method decrypts the `encrypted_data` with the authentication key provided during initialization.

   This method raises `cryptography.fernet.InvalidToken` if the authentication does not match with the one used for
   encryption.

   *Parameters*: *`raw_data` - The encrypted (binary) data*

3. Method `get_salt_string(self) -> str`

   This method returns the Base64-encoded string of the salt.

   *Parameters*: *No parameter required*

#### Other methods

1. Initialization `Cryptographer(self, salt: bytes, auth_key: bytes, encrypt: bool = True) -> None`

   This method is rarely called directly, as all instances should be initialized with `Cryptographer.make_encrypter` and
   `Cryptographer.make_decrypter`.

   *Parameters*:

   * *`salt` - Salt for the key derivation function*

   * *`auth_key` - Authentication key*

   * *`encrypt` - Whether this instance encrypts (`True`) or decrypts (`False`)*

2. Static method `make_encrypter(key: str) -> Cryptographer`

   This method is used to make an encrypting `Cryptographer` with `key` as the authentication key.

   * *`key` - Authentication key*

3. Static method `make_decrypter(key: str) -> Cryptographer`

   This method is used to make a decrypting `Cryptographer` with `key` as the authentication key.

   * *`key` - Authentication key*

4. Static method `make_salt() -> bytes`

   This method returns a 16-byte-long string to be used as salt for the key derivation function.

   *Parameters*: *No parameter required*

5. Static method `encode_salt(salt: bytes) -> str`

   This method encodes the binary `salt` into a Base64-encoded string.

   *Parameters*: *`salt` - Binary salt*

6. Static method `decode_salt(salt: str) -> bytes`

   This method decodes the Base64-encoded string `salt` into its binary.

   *Parameters*: *`salt` - Base64-encoded salt*

7. Static method `make_kdf(salt: bytes) -> PBKDF2HMAC`

   This method returns a key derivation function from the `salt` provided.

   *Parameters*: *`salt` - Binary salt for the key derivation function*

8. Static method `make_fernet(key: bytes) -> Fernet`

   This method returns a `Fernet` instance with the derived key `key`.

   *Parameters*: *`key` - The derived key (from key derivation function)*

### Standalone functions

1. Function `load_installed_modules(config: dict[str, ...]) -> list[tuple[click.Command, str]]`

   This function is intended for internal use only. It takes in the core config (passed in by the decorator), and
   returns a list of `click.Command` objects of added modules.

   *Parameters*: *No parameter required*

2. Function `load_core_commands() -> list[tuple[click.Command, str]]`

   This function is intended for internal use only. It is a helper function, which returns all core commands defined in
   the module.

   *Parameters*: *No parameter required*

3. Function `initialise_core_logger(logging_path: str) -> logging.Logger`

   This function is intended for internal use only. It is called by the core CLI when the application starts to
   initialize the logger.

   *Parameters*: *`logging_path` - Path to log file*

### Command documentation

1. Command `add`

* **Usage**: `helper add <MODULES>` where `<MODULES>` are names of modules you wish to add.

* **Notes**: This command is used to add any modules that are not added yet.

2. Command `remove`

* **Usage**: `helper remove <MODULES>` where `<MODULES>` are names of modules you wish to remove.

* **Notes**: This command is used to remove any modules that are added.

3. Command `list`

* **Usage**: `helper list`

* **Notes**: This command is used to list all installed modules (added or not added)
