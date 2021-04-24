import csv
import datetime
import io
import json
from urllib.error import HTTPError
from urllib.request import urlopen
from pathlib import Path
import re
import logging

from dateutil.parser import parse

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

origin_date = datetime.datetime(day=2, month=12, year=2020)


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


def get_source_file(url: str, force: bool = False) -> list:
    filename = Path(url).name
    source_file_location = MODULE_DIR / "Cache" / filename
    if not force and source_file_location.is_file():
        with open(source_file_location) as fp:
            return fp.readlines()
    raw_data = list(urlopen(url))
    string_data = list(map(lambda s: str(s, "utf-8"), raw_data))
    with open(source_file_location, "w") as fp:
        fp.writelines(string_data)
    return string_data


latest_date = datetime.datetime.today()
while True:
    try:
        get_source_file(create_source_url(latest_date.strftime("%m-%d-%Y")))
    except HTTPError:
        latest_date -= datetime.timedelta(days=1)
    else:
        break


def parse_source_data(source_data: list[str]) -> list:
    concat = "".join(source_data)
    buffer = io.StringIO(concat)
    csv_parsed_data = csv.reader(buffer)
    return list(csv_parsed_data)


def extract_source_data(parsed_data: list[str], cache_file: PathLike = None, force: bool = False) -> dict[str, list]:
    # Remove header
    parsed_data.pop(0)
    starting_index = 7
    number_of_field = 4
    if not force and cache_file is not None and Path(cache_file).is_file():
        with open(cache_file) as fp:
            return json.load(fp)
    data = dict()
    for entry in parsed_data:
        entry = list(map(lambda s: "0" if s == "" else s, entry))
        country_name = entry[3]
        if country_name in data.keys():
            for i in range(number_of_field):
                data[country_name][i] += int(entry[starting_index + i])
        else:
            data[country_name] = list(map(int, entry[starting_index:starting_index + number_of_field]))
    if cache_file is not None:
        with open(cache_file, "w") as fp:
            json.dump(data, fp)
    return data


def get_data_for_date(date_string: str, force: bool = False):
    date_string = normalise_datetime(date_string)
    url = create_source_url(date_string)
    source_file = get_source_file(url, force)
    parsed_source_file = parse_source_data(source_file)
    cache_filename = CACHE_DIR / f"extracted-{Path(url).name.split('.')[0]}.json"
    return extract_source_data(parsed_source_file, cache_filename, force)


def cache_data(no_of_days: int = 365, force: bool = False) -> None:
    date = datetime.datetime.today()
    date_string = date.strftime("%m-%d-%Y")
    origin_date = datetime.datetime(day=3, month=12, year=2020)
    if (date - origin_date).days < no_of_days:
        no_of_days = (date - origin_date).days
    while True:
        try:
            get_source_file(create_source_url(date_string))
        except HTTPError:
            date -= datetime.timedelta(days=1)
            date_string = date.strftime("%m-%d-%Y")
        else:
            break
    for i in range(no_of_days):
        print(f"\rDownloading for {date_string}... ({i+1}/{no_of_days})", end="")
        try:
            get_data_for_date(date_string, force)
        except HTTPError:
            pass
        date -= datetime.timedelta(days=1)
        date_string = date.strftime("%m-%d-%Y")
    print()
