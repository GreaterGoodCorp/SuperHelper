import sys
import pytest

from SuperHelper.Core import main_entry


@pytest.fixture(autouse=True)
def create_and_clean_config():
    sys.argv = ["helper", "add", "Stenographer"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()
    yield
