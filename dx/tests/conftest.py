import random
import string

import pandas as pd
import pytest
from IPython.core import formatters
from IPython.core.formatters import BaseFormatter


@pytest.fixture
def pandas_formatter() -> BaseFormatter:
    class PandasTableSchemaFormatter(BaseFormatter):
        print_method = "_repr_data_resource_"
        _return_type = (dict,)

    return PandasTableSchemaFormatter()


@pytest.fixture
def ipython_display_formatters(pandas_formatter: BaseFormatter) -> dict:
    """
    Creates mock ipython display formatters for standard media types
    and the pandas data resource media type.
    """
    return {
        "application/pdf": formatters.PDFFormatter(),
        "application/javascript": formatters.JavascriptFormatter(),
        "application/json": formatters.JSONFormatter(),
        "application/vnd.dataresource+json": pandas_formatter,
        "text/html": formatters.HTMLFormatter(),
        "text/latex": formatters.LatexFormatter(),
        "text/markdown": formatters.MarkdownFormatter(),
        "text/plain": formatters.PlainTextFormatter(),
        "image/jpeg": formatters.JPEGFormatter(),
        "image/png": formatters.PNGFormatter(),
        "image/svg+xml": formatters.SVGFormatter(),
    }


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
