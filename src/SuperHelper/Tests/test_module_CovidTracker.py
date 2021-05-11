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
