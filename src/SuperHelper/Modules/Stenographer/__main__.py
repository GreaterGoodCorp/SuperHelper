import bz2
import functools
import io
import logging
import re

import click
import cryptography.fernet
from PIL import Image

from SuperHelper.Core.Config import Config, pass_config
from SuperHelper.Core.Utils import BitOps, Cryptographer, ImageOps

MODULE_NAME: str = "Stenographer"
pass_config_no_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=False)
pass_config_with_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=True)
__name__ = f"SuperHelper.Builtins.{MODULE_NAME}"
logger = logging.getLogger(__name__)


class Header:
    """Provides for the preparation of the creation of steganography."""

    # Padding character, used when header is too short
    # after writing all the required metadata
    padding_character: str = "-"

    # Separator is used to make regex easier
    separator: str = "?"

    # Various types of length for the header
    maximum_data_length: int = 8
    maximum_flag_length: int = 3
    salt_length: int = 24
    separator_length: int = 2
    header_length: int = maximum_data_length + maximum_flag_length + salt_length + separator_length

    # Regex pattern of the header
    # data_length?flag?salt
    pattern: str = r"(\d{1,8})\?(\d{1,3})\?"
    hash_pattern: str = r"((?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==" + \
                        r"|[A-Za-z0-9+/]{3}=)?)"
    pattern: re.Pattern = re.compile(f"^{pattern + hash_pattern}$")

    def __str__(self) -> str:
        """Returns the header."""
        return self.header

    def __repr__(self) -> str:
        """Same as __str__, returns the header."""
        return str(self)

    def __init__(self, data_length: int, compression: int, density: int,
                 salt: str) -> None:
        self.header: str = str()
        self.data_length: int = data_length
        self.compression: int = compression
        self.density: int = density
        self.salt: str = salt

        self.generate()

    def generate(self) -> None:
        """
        Generates a header created from input_file given during
        Header initialisation.

        There is no need to call this method, unless any metadata has been
        modified after initialisation.
        """
        # Create a flag from compression level and density level.
        # Bit 6 - 2: Compression level (0 (no compression) - 9)
        # Bit 1 - 0: Density level (1 - 3)
        flag = (self.compression << 2) + self.density

        result_header = Header.separator.join(
            (str(self.data_length), str(flag), self.salt))

        assert Header.pattern.match(result_header)

        # Assign as a class attribute
        self.header = result_header


def validate_header(b: bytes) -> bool:
    try:
        s = str(b, "utf-8")
        return True if Header.pattern.match(s) else False
    except UnicodeDecodeError:
        return False


@pass_config_no_lock()
def build_header(config: dict[str, ...], data_length: int, salt: str, compression: int, density: int) -> Header:
    compression = config["default_compression"] if compression not in config["available_compression"] else compression
    density = config["default_density"] if density not in config["available_density"] else density
    return Header(data_length, compression, density, salt)


def parse_header(b: bytes) -> Header:
    if not validate_header(b):
        raise ValueError("Invalid header!")

    header_match = Header.pattern.match(str(b, "utf-8"))

    hdr_data_length = int(header_match[1])
    hdr_flag = int(header_match[2])
    hdr_salt = header_match[3]
    hdr_density = hdr_flag & 0b11
    hdr_compression = (hdr_flag - hdr_density) >> 2

    # Build and return a Header object
    return build_header(
        data_length=hdr_data_length,
        compression=hdr_compression,
        density=hdr_density,
        salt=hdr_salt
    )


@pass_config()
def patch_config(config: Config) -> None:
    cfg = {
        "available_compression": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "available_density": [1, 2, 3],
        "default_compression": 9,
        "default_density": 1,
        "default_auth_key": "bGs21Gt@31",
        "flag_show_image_on_completion": False,
        "flag_file_open_mode": "rb",
    }
    config.apply_module_patch(MODULE_NAME, cfg)


@pass_config_no_lock()
def write_steganography(input_file: io.IOBase, image_file: Image.Image, output_file: io.IOBase, auth_key: str,
                        compression: int, density: int, show_image_on_completion: bool,
                        config: dict[str, ...] = None) -> int:
    auth_key = config["default_auth_key"] if auth_key is None else auth_key
    compression = config["default_compression"] if compression not in config["available_compression"] else compression
    density = config["default_density"] if density not in config["available_density"] else density
    show_image_on_completion = config["flag_show_image_on_completion"] \
        if show_image_on_completion is None else show_image_on_completion

    input_file.seek(0)
    data = input_file.read()
    if data is None:
        logger.error("Input file is not readable!")
        return 1
    if len(data) == 0:
        logger.error("Input file is empty or exhausted!")
        return 1

    if compression > 0:
        # Compress using the builtin bzip2 library
        data = bz2.compress(data, compresslevel=compression)

    crypto = Cryptographer.make_encrypter(auth_key)
    data = crypto.encrypt(data)

    # Craft the finished input_file
    header = build_header(
        data_length=len(data),
        compression=compression,
        density=density,
        salt=crypto.get_salt_string(),
    )
    # 2. Serialise header and prepend input_file with header
    data = bytes(header.header, "utf-8") + data

    try:
        pix = image_file.load()
    except Exception or BaseException:
        logger.exception("Cannot load image_file file!")
        return 1

    x_dim, y_dim = image_file.size

    # Make sure there are enough space to store all bits
    no_of_pixel = x_dim * y_dim
    no_of_rgb = no_of_pixel * 3
    no_of_storable_bit = no_of_rgb * density
    no_of_stored_bit = len(data) * 8
    if no_of_storable_bit < no_of_stored_bit:
        # If there are not enough, raise error
        logger.error("Data is too big to be stored!")
        return 1

    x, y, count, bit_loc = 0, 0, 0, density
    current_pix = list(pix[0, 0])

    # Firstly, iterate through all the bytes to be written
    for byte in data:
        # Secondly, iterate through all the bits of the given byte
        for i in range(8):
            # Thirdly, check if the bit is set
            # If bit is set
            if BitOps.is_bit_set(byte, i):
                # Check if the bit at the current location in the image_file is set
                # If unset then set it, otherwise unchanged
                current_pix[count] = BitOps.set_bit(current_pix[count], bit_loc)
            # If bit is unset
            else:
                # Check if the bit at the current location in the image_file is set
                # If set then unset it, otherwise unchanged
                current_pix[count] = BitOps.unset_bit(current_pix[count], bit_loc)
            # Move to the next bit
            # by decrementing index
            bit_loc -= 1
            # If reached the final bit
            if bit_loc == -1:
                # Move to the next integer
                # by incrementing the count
                count += 1
                # Reset density
                bit_loc = density
                # If reached the last RGB
                if count == 3:
                    # Save pixel
                    pix[x, y] = tuple(current_pix)
                    # Reset count
                    count = 0
                    y += 1
                    # If the entire row of pixel is written
                    if y == y_dim:
                        # Move on to the next row and reset
                        y = 0
                        x += 1
                    # Request new pixel to be written
                    current_pix = list(pix[x, y])

    try:
        image_file.save(output_file, "png")
    except OSError:
        logger.exception("Cannot save image_file to output_file file!")
        return 1

    if show_image_on_completion:
        ImageOps.show_image(image_file)

    input_file.close()
    image_file.close()
    output_file.close()

    return 0


@pass_config_no_lock()
def extract_header(config: dict[str, ...], image: Image.Image) -> Header:
    pix = image.load()
    y_dim = image.size[1]
    x, y, count = 0, 0, 0
    result_data = b""
    density = 1

    # Firstly, the header is retrieved by reading for its known length.
    # Since the density is unknown, check all density one by one.
    while density in config["available_density"]:
        bit_loc = density
        while len(result_data) < Header.header_length:
            byte = 0
            # Read every single bit
            # Iterate through every single bit of the byte
            for i in range(8):
                # If bit is set, set the corresponding bit of 'byte'
                if pix[x, y][count] & (1 << bit_loc):
                    byte += (1 << (7 - i))
                # Move to the next bit by decrement bit index
                bit_loc -= 1
                # If all readable bits of the colour integer are consumed
                if bit_loc == -1:
                    # Move to the next RGB and reset the bit index
                    count += 1
                    bit_loc = density
                    # If the entire pixel is read
                    if count == 3:
                        # Move to the next pixel in the row and reset the count
                        count = 0
                        y += 1
                        # If the entire row of pixels is read
                        if y == y_dim:
                            # Move to the next row and reset row index
                            y = 0
                            x += 1
            # Convert the single byte (integer) to bytes
            # By design, the resulting input_file is strictly stored in 1 byte
            # and endianness does not matter since it is only 1 byte
            result_data += byte.to_bytes(1, "big")
        # If header is invalid
        # e.g wrong density
        try:
            # Invalid header has undecodable byte
            return parse_header(result_data)
        except ValueError:
            # Hence, switch to the next possible density
            # Reset all values to original
            density += 1
            result_data = b""
            x, y, count = 0, 0, 0


@pass_config_no_lock()
def extract_steganography(input_file: io.IOBase, output_file: io.IOBase, auth_key: str) -> int:
    try:
        image = Image.open(input_file)
    except Image.UnidentifiedImageError:
        logger.exception(f"Not an image_file!")
        return 1

    header = extract_header(image)
    pix = image.load()
    y_dim = image.size[1]
    data_length = Header.header_length + header.data_length
    x, y, count = 0, 0, 0
    result_data = b""
    bit_loc = header.density

    # Attempt to read input_file
    while len(result_data) < data_length:
        byte = 0
        # Read every single bit
        # Iterate through every single bit of the byte
        for i in range(8):
            # If bit is set, set the corresponding bit of 'byte'
            if pix[x, y][count] & (1 << bit_loc):
                byte += (1 << (7 - i))
            # Move to the next bit by decrement bit index
            bit_loc -= 1
            # If all readable bits of the colour integer are consumed
            if bit_loc == -1:
                # Move to the next RGB and reset the bit index
                count += 1
                bit_loc = header.density
                # If the entire pixel is read
                if count == 3:
                    # Move to the next pixel in the row and reset the count
                    count = 0
                    y += 1
                    # If the entire row of pixels is read
                    if y == y_dim:
                        # Move to the next row and reset row index
                        y = 0
                        x += 1
        # Convert the single byte (integer) to bytes
        # By design, the resulting input_file is strictly stored in 1 byte
        # and endianness does not matter since it is only 1 byte
        result_data += byte.to_bytes(1, "big")

    # Strip header by slicing its known length
    result_data = result_data[Header.header_length:]

    # Decrypt input_file
    crypto = Cryptographer.make_decrypter(header.salt, auth_key)
    try:
        # 5. Store decrypted input_file
        result_data = crypto.decrypt(result_data)
    except cryptography.fernet.InvalidToken:
        logger.exception("Invalid authentication key!")
        return 1

    # If compressed (as indicated by the header), decompress it
    if header.compression > 0:
        result_data = bz2.decompress(result_data)

    # Write input_file to output_file file objects
    # Iterate through all file objects
    output_file.write(result_data)
    try:
        output_file.write(result_data)
        output_file.close()
    except IOError:
        logger.exception("Data cannot be writen")
        return 1

    return 0


@click.group("steg")
def main() -> None:
    """Applies steganography on images."""
    patch_config()


@main.command("create", help="Creates steganography")
@click.option("-i", "--image_file", help="Path to custom image_file file", type=click.File("rb"), required=True)
@click.option("-k", "--key", help="The authentication key", type=str)
@click.option("-c", "--compress", help="Compression level of the steganography", type=int, default=-1)
@click.option("-d", "--density", help="Density of the steganography (from 1 to 3)", type=int, default=-1)
@click.option("-o", "--output_file", help="Path to output file", type=click.File("wb"), required=True)
@click.option("--show-image_file", help="Whether to show image_file on creation", type=bool, default=False)
@click.argument("input_file", type=click.File("rb"), required=True)
@pass_config_no_lock()
def create(image_file: io.IOBase, key: str, compress: int, density: int, output_file: io.IOBase, show_image: bool,
           input_file: io.IOBase, config: dict[str, ...]):
    if density not in config["available_density"]:
        raise click.exceptions.BadOptionUsage(
            "density", "Density must be from 1 to 3!")

    if compress not in config["available_compress"]:
        raise click.exceptions.BadOptionUsage(
            "density", "Density must be from 0 (no compress) to 9!")
    key = config["default_auth_key"] if key is None else key

    try:
        image = Image.open(image_file)
    except Image.UnidentifiedImageError:
        logger.exception("Not an image file!")
        return 1

    # Perform operation
    return write_steganography(input_file, image, output_file, key, compress, density, show_image)


@main.command("extract", help="Extracts steganography")
@click.option("-k", "--key", help="The authentication key", type=str)
@click.option("-o", "--output_file", help="Path to output file", type=click.File("wb"), required=True)
@click.argument("steganography", required=True, type=click.File("wb"))
def extract(key: str, output_file: io.IOBase, steganography: io.IOBase):
    return extract_steganography(steganography, output_file, key)
