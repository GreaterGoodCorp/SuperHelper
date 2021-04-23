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


def normalise_datetime(date_string: str) -> str:
    try:
        return parse(date_string, dayfirst=True).strftime("%m-%d-%Y")
    except ValueError:
        raise ValueError("Invalid date format")


def create_source_url(date_string: str) -> str:
    if not re.match(r"^(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])-20\d\d$", date_string):
        raise ValueError("Invalid date format, must be MM-DD-YYY! Try using normalise_datetime()!")
    gh_branch_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master"
    source_path = "/csse_covid_19_data/csse_covid_19_daily_reports/"
    file_name = f"{date_string}.csv"
    return gh_branch_url + source_path + file_name


def get_source_file(url: str) -> list:
    filename = Path(url).name
    source_file_location = MODULE_DIR / "Cache" / filename
    if source_file_location.is_file():
        with open(source_file_location) as fp:
            return fp.readlines()
    raw_data = list(urlopen(url))
    string_data = list(map(lambda s: str(s, "utf-8"), raw_data))
    with open(source_file_location, "w") as fp:
        fp.writelines(string_data)
    return string_data


def parse_source_data(source_data: list[str]) -> list:
    concat = "".join(source_data)
    buffer = io.StringIO(concat)
    csv_parsed_data = csv.reader(buffer)
    return list(csv_parsed_data)


def extract_source_data(parsed_data: list[str], cache_filename: PathLike = None) -> dict[str, list]:
    # Remove header
    parsed_data.pop(0)
    starting_index = 7
    number_of_field = 4
    if cache_filename is not None and Path(cache_filename).is_file():
        with open(cache_filename) as fp:
            return json.load(fp)
    data = dict()
    for entry in parsed_data:
        entry = list(map(lambda s: "0" if s == "" else s, entry))
        country_name = entry[3]
        if country_name in data.keys():
            for i in range(number_of_field):
                data[country_name][i] += int(entry[starting_index+i])
        else:
            data[country_name] = list(map(int, entry[starting_index:starting_index+number_of_field]))
    if cache_filename is not None:
        with open(cache_filename, "w") as fp:
            json.dump(data, fp)
    return data
