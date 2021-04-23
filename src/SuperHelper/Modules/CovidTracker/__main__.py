import csv
import io
import json
from urllib.request import urlopen
from dateutil.parser import parse
from pathlib import Path
import re
import logging

from SuperHelper import AppDir
from SuperHelper.Core.Utils import PathLike

MODULE_NAME: str = "CovidTracker"
MODULE_DIR = AppDir / MODULE_NAME
MODULE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = MODULE_DIR / "Cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
__name__ = f"SuperHelper.Modules.{MODULE_NAME}"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
