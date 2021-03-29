# This file defines SteganographyConfig class, which is used to
# configure all operations of the Steganography Library.


def initialise_default_module_config():
    return {
        "available_compression": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "available_density": [1, 2, 3],
        "default_compression": 9,
        "default_density": 1,
        "default_auth_key": "bGs21Gt@31",
        "flag_close_on_exit": True,
        "flag_show_image_on_completion": False,
        "flag_file_open_mode": "rb",
    }


SteganographyConfig: dict = initialise_default_module_config()