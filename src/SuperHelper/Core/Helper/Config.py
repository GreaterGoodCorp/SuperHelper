# This module defines the config loader functions, which can be used by all modules

# Pathlib.Path is used to initialise paths
from pathlib import Path

# JSON is used serialise and deserialise config objects
from json import load, dump

# Define config class
class AppConfig:
    VERBOSE = False
    IGNORE_ERROR = False
    
    CONFIG_FILENAME = ".shrc"
    CONFIG_PATH = Path.home() / CONFIG_FILENAME

def load_all_config():
    # Try-catch the file opening
    try:
        with open(CONFIG_PATH) as fp:
            # Deserialise JSON to Python's dict
            return load(fp)
    except OSError:
        if not AppConfig.IGNORE_ERROR:
            pass
        pass

def load_cli_config():
    
            
