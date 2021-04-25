import datetime
from urllib.error import HTTPError
from pathlib import Path

import pytest

from SuperHelper.Tests import *
from SuperHelper.Modules.CovidTracker.__main__ import *


class TestCovidTracker:
    @staticmethod
    @pytest.fixture()
    def setup():
        run("add CovidTracker")

    @staticmethod
    def test_validate_setup(setup):
        assert "CovidTracker" in run("list").output

    @staticmethod
    @pytest.fixture()
    def get_valid_date():
        return (datetime.datetime.today() + datetime.timedelta(days=-2)).strftime("%m-%d-%Y")

    @staticmethod
    @pytest.fixture()
    def get_invalid_date():
        return (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%m-%d-%Y")

    @staticmethod
    @pytest.fixture()
    def get_valid_url(get_valid_date):
        return create_source_url(get_valid_date)

    @staticmethod
    @pytest.fixture()
    def get_invalid_url(get_invalid_date):
        return create_source_url(get_invalid_date)

    @staticmethod
    @pytest.fixture()
    def get_cache_filename(get_valid_url):
        return CACHE_DIR / f"extracted-{Path(get_valid_url).name.split('.')[0]}.json"

    @staticmethod
    @pytest.fixture()
    def get_raw_data(get_valid_url):
        return get_source_file(get_valid_url)

    @staticmethod
    @pytest.fixture()
    def get_parsed_data(get_raw_data):
        return parse_source_data(get_raw_data)

    @staticmethod
    def test_normalise_datetime(get_valid_date, get_invalid_date):
        assert normalise_datetime("31-12-2021")
        assert normalise_datetime(get_valid_date)
        assert normalise_datetime("31-12-1121")
        with pytest.raises(ValueError):
            normalise_datetime("32-12-2021")

    @staticmethod
    def test_create_source_url(get_valid_date, get_invalid_date):
        assert create_source_url("12-31-2021")
        assert create_source_url(get_valid_date)
        assert create_source_url("12-31-2099")
        with pytest.raises(ValueError):
            create_source_url("12-31-1999")
        with pytest.raises(ValueError):
            create_source_url("12-31-1999")

    @staticmethod
    def test_get_source_file(get_valid_url, get_invalid_url):
        assert len(get_source_file(get_valid_url)) != 0
        assert len(get_source_file(get_valid_url)) != 0
        with pytest.raises(HTTPError):
            get_source_file(get_invalid_url)

    @staticmethod
    def test_parse_source_file(get_raw_data):
        assert len(parse_source_data(get_raw_data)) != 0

    @staticmethod
    def test_extract_source_data(get_parsed_data, get_cache_filename):
        assert len(extract_source_data(get_parsed_data, get_cache_filename)) != 0
        assert len(extract_source_data(get_parsed_data, get_cache_filename)) != 0
        assert len(extract_source_data(get_parsed_data)) != 0

    @staticmethod
    def test_cache_data():
        assert cache_data(1, True) is None

    @staticmethod
    def test_cache():
        assert run("covid cache -f 2").exit_code == 0
        assert run("covid cache 2").exit_code == 0

    @staticmethod
    def test_tally():
        assert run("covid tally Singapore").exit_code == 0
        assert run("covid tally singapore").exit_code == 2

        assert run("covid tally -d 12.02.2021 Singapore").exit_code == 0
        assert run("covid tally -d fast Singapore").exit_code == 2

    @staticmethod
    def test_plot():
        assert run("--debug covid plot -cdra -n 2 Singapore").exit_code == 0
        assert run("--debug covid plot -c -n 2 Singapore").exit_code == 0
        assert run("--debug covid plot -d -n 2 Singapore").exit_code == 0
        assert run("--debug covid plot -r -n 2 Singapore").exit_code == 0
        assert run("--debug covid plot -a -n 2 Singapore").exit_code == 0
        assert run("--debug covid plot -n 2 Singapore").exit_code == 1
        assert run("--debug covid plot -cdra -n 2 singapore").exit_code == 2
