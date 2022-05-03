import random
import string

import pandas as pd
import pytest
from IPython.core import formatters
from IPython.core.formatters import BaseFormatter, DisplayFormatter
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.testing import tools


@pytest.fixture
def get_ipython() -> TerminalInteractiveShell:
    if TerminalInteractiveShell._instance:
        return TerminalInteractiveShell.instance()

    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "col_1": list("aaa"),
            "col_2": list("bbb"),
            "col_3": list("ccc"),
        }
    )
    return df


@pytest.fixture
def sample_large_dataframe() -> pd.DataFrame:
    """
    Generates a random assortment of values of different data types,
    and returns a larger dataframe than the `sample_dataframe` fixture.
    """
    n_rows = 100_000
    data = {
        "float_col": [random.randint(0, 100) for _ in range(n_rows)],
        "int_col": [random.random() for _ in range(n_rows)],
        "bool_col": [random.choice([True, False]) for _ in range(n_rows)],
        "str_col": [
            "".join(random.sample(string.ascii_uppercase, 3)) for _ in range(n_rows)
        ],
        "date_col": [
            pd.Timestamp("now") - pd.Timedelta(hours=random.randint(-100, 100))
            for _ in range(n_rows)
        ],
    }
    return pd.DataFrame(data)
