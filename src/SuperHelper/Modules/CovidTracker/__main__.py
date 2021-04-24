import csv
import datetime
import io
import json
import sys
from copy import deepcopy
from urllib.error import HTTPError
from urllib.request import urlopen
from pathlib import Path
import re
import logging

from dateutil.parser import parse
import click

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

__all__ = [
    "normalise_datetime",
    "create_source_url",
    "get_source_file",
    "parse_source_data",
    "extract_source_data",
    "get_country_data",
    "get_data_for_date",
    "cache_data",
]


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
    if not re.match(r"^(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])-20\d\d$", date_string):
        raise ValueError("Invalid date format, must be MM-DD-YYY! Try using normalise_datetime()!")
    url = create_source_url(date_string)
    source_file = get_source_file(url, force)
    parsed_source_file = parse_source_data(source_file)
    cache_filename = CACHE_DIR / f"extracted-{Path(url).name.split('.')[0]}.json"
    return extract_source_data(parsed_source_file, cache_filename, force)


def get_country_data(country: str, start_date: datetime.datetime = None, end_date: datetime.datetime = None):
    if end_date is None or end_date > latest_date:
        end_date = latest_date
    if start_date is None or start_date < origin_date:
        start_date = origin_date
    result = dict()
    for i in range((end_date - start_date).days + 1):
        date_string = (start_date + datetime.timedelta(days=i)).strftime("%m-%d-%Y")
        data = get_data_for_date(date_string)
        country_data = data.get(country, None)
        if country_data is not None:
            result[date_string] = country_data
        else:
            raise ValueError(country)
    return result


def cache_data(no_of_days: int = 365, force: bool = False) -> None:
    date = deepcopy(latest_date)
    date_string = date.strftime("%m-%d-%Y")
    if (date - origin_date).days < no_of_days:
        no_of_days = (date - origin_date).days
    for i in range(no_of_days):
        print(f"\rDownloading for {date_string}... ({i + 1}/{no_of_days})", end="")
        try:
            get_data_for_date(date_string, force)
        except HTTPError:
            pass
        date -= datetime.timedelta(days=1)
        date_string = date.strftime("%m-%d-%Y")
    print()


def validate_date(value, *_, **__):
    try:
        if value == "latest":
            return latest_date.strftime("%m-%d-%Y")
        else:
            d = normalise_datetime(value)
            if datetime.datetime.strptime(d, "%m-%d-%Y") > latest_date:
                logger.warning(f"Date for date '{d}' is not available. Using the latest data...")
                return latest_date.strftime("%m-%d-%Y")
            return d
    except ValueError:
        raise click.BadParameter("Invalid date format")


@click.group("covid")
def main():
    """Shows and plots COVID-19 data."""
    pass


@main.command("tally")
@click.option("-d", "--date", default="latest", help="The date of the tally.", type=validate_date)
@click.argument("countries", nargs=-1, type=str, required=True)
def tally(date, countries):
    """Shows COVID-19 tally for countries."""
    click.echo(f"Selected date (MM-DD-YYYY) is {date}")
    date_obj = datetime.datetime.strptime(date, "%m-%d-%Y")
    data = []
    for ct in countries:
        try:
            data.append(get_country_data(ct, date_obj, date_obj)[date])
        except ValueError as ex:
            raise click.BadParameter(f"Country '{ex.args[0]}' is not found!")
    click.echo(f"{'Country':<15} {'Confirmed':<15} {'Death':<15} {'Recovered':<15} {'Active':<15}")
    for ct, d in zip(countries, data):
        click.echo(f"{ct:<15} {d[0]:<15} {d[1]:<15} {d[2]:<15} {d[3]:<15}")
    sys.exit(0)
