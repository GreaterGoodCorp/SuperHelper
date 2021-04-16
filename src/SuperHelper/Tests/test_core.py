import sys

import pytest

from SuperHelper.Core import main_entry


def test_main_entry():
    sys.argv = ["helper", "--version"]
    with pytest.raises(SystemExit, match="0"):
        main_entry()
