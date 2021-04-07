# Builtin modules
from os import path, getcwd
from sys import stdout as std

# Non-builtin modules
import click

from SuperHelper.Modules.Stenographer.core import SteganographyConfig as Config
from SuperHelper.Modules.Stenographer.core.steg import write_steganography, extract_steganography
# Internal modules
from SuperHelper.Modules.Stenographer.helper import raw_open, open_image
from SuperHelper.Core.Config import load_module_config, save_module_config


@click.group("steg")
def main():
    """Stenographer is a program that deals with pictorial steganography."""
    Config.update(load_module_config("SuperHelper.Modules.Stenographer"))
    save_module_config("SuperHelper.Modules.Stenographer", Config)
    pass


@main.command(
    "create",
    help="Create steganography"
)
@click.option(
    "-i",
    "--image",
    help="Path to custom image file",
    type=click.Path(True, True, False),
    required=True
)
@click.option(
    "-k",
    "--key",
    help="The authentication key",
    type=str,
    default=Config["default_auth_key"]
)
@click.option(
    "-c",
    "--compress",
    help="Compression level of the steganography",
    type=int,
    default=Config["default_compression"]
)
@click.option(
    "-p",
    "--pack",
    help="Density of the steganography (from 1 to 3)",
    type=int,
    default=Config["default_density"]
)
@click.option(
    "-o",
    "--output",
    help="Path to output file",
    type=click.Path(False)
)
@click.option(
    "--show-image",
    help="Whether to show image on creation",
    type=bool,
    default=False,
)
@click.argument("data", type=click.Path(True, True, False), required=True)
def create(
    image: str,
    key: str,
    compress: int,
    pack: int,
    output: str,
    show_image: bool,
    data: str
):
    if pack not in Config["available_density"]:
        raise click.exceptions.BadOptionUsage(
            "pack", "Density must be from 1 to 3!")

    if not path.isabs(image):
        # Get the absolute path for the user-specified image
        image = path.join(getcwd(), *path.split(image))

    if not path.isabs(data):
        # Get the absolute path for the user-specified data file
        data = path.join(getcwd(), *path.split(data))

    if output is None:
        # Get the absolute path for the default output file
        # Default is the name of data file, change extension to .png
        name_no_ext = path.splitext(data)[0]
        output = name_no_ext + ".png"
    elif not path.isabs(output):
        # Get the absolute path for the user-specified output file
        output = path.join(getcwd(), *path.split(output))

    # Attempt to read files
    try:
        image_fileobject = raw_open(image)
    except IOError:
        raise click.FileError(image)
    try:
        data_fileobject = raw_open(data)
    except IOError:
        raise click.FileError(data)
    try:
        output_fileobject = raw_open(output, "wb")
    except IOError:
        raise click.FileError(output)

    # Perform operation
    write_steganography(
        data_fileobject,
        open_image(image_fileobject),
        output_fileobject,
        auth_key=key,
        compression=compress,
        density=pack,
        show_image_on_completion=show_image,
    )


@main.command(
    "extract",
    help="Extract steganography_modified",
)
@click.option(
    "-k",
    "--key",
    help="The authentication key",
    type=str,
    default=Config["default_auth_key"],
)
@click.option(
    "-o",
    "--output",
    help="Path to output file",
    type=click.Path(False)
)
@click.option(
    "-s",
    "--stdout",
    help="Additionally output to stdout",
    type=bool,
    default=False
)
@click.argument(
    "steganography",
    required=True,
    type=click.Path(True, True, False)
)
def extract(key: str, output: str, stdout: bool, steganography: str):
    if not path.isabs(steganography):
        # Get the absolute path for the steganography_modified
        steganography = path.join(getcwd(), *path.split(steganography))

    if output is None:
        # Get the absolute path of the default output file
        # Default is the name of the steganography_modified, extension-stripped
        output = path.splitext(steganography)[0]

    # Attempt to read files
    try:
        steganography_fileobject = raw_open(steganography)
    except IOError:
        raise click.FileError(steganography)
    try:
        output_fileobject = raw_open(output)
    except IOError:
        raise click.FileError(output)

    # Compile output files
    output_object = [output_fileobject]
    if stdout:
        output_object.append(std)

    extract_steganography(
        steganography_fileobject,
        output_object,
        auth_key=key,
    )
