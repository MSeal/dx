import duckdb
import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.testing import tools

from dx.datatypes.main import random_dataframe
from dx.settings import get_settings
from dx.types import DEXFilterSettings
from dx.utils.formatting import normalize_index_and_columns
from dx.utils.tracking import DXDataFrame

settings = get_settings()


def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return

    skip_benchmarks = pytest.mark.skip(
        reason="benchmark marker not selected, use `-m benchmark` to include this test"
    )
    for item in items:
        if "benchmark" in item.keywords:
            item.add_marker(skip_benchmarks)


@pytest.fixture
def get_ipython() -> TerminalInteractiveShell:
    if TerminalInteractiveShell._instance:
        return TerminalInteractiveShell.instance()

    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = TerminalInteractiveShell.instance(config=config)
    # clear out any lingering variables between tests
    shell.user_ns = {}
    return shell


@pytest.fixture
def sample_db_connection() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    yield conn
    conn.close()


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
def sample_random_dataframe() -> pd.DataFrame:
    return random_dataframe()


@pytest.fixture
def sample_cleaned_random_dataframe(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    return normalize_index_and_columns(sample_random_dataframe)


@pytest.fixture
def sample_groupby_dataframe(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This will generate a dataframe with two MultiIndexes:
    - one at .index with 2 levels: keyword_column and integer_column
    - one at .columns with the min/max values of any remaining columns
    """
    return sample_random_dataframe.groupby(["keyword_column", "integer_column"]).agg(["min", "max"])


@pytest.fixture
def sample_resampled_dataframe(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    return sample_random_dataframe.resample("1D", on="datetime_column").min()


@pytest.fixture
def sample_resampled_groupby_dataframe(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        sample_random_dataframe.groupby("keyword_column").resample("1D", on="datetime_column").min()
    )


@pytest.fixture
def sample_groupby_series(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This will generate a pd.Series with a MultiIndex and one column whose name also appears in the MultiIndex names.
    """
    return sample_random_dataframe.groupby(
        ["keyword_column", "integer_column"]
    ).float_column.value_counts()


@pytest.fixture
def sample_multiindex_series(sample_random_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This will generate a pd.Series with a MultiIndex and one column whose name does not appear in the MultiIndex names.
    """
    return sample_random_dataframe.groupby(["keyword_column", "integer_column"]).float_column.mean()


@pytest.fixture
def sample_large_dataframe() -> pd.DataFrame:
    """
    Generates a dataframe that is within the MAX_ROWS/MAX_COLUMNS limits,
    but has large values that should still exceed MAX_RENDER_SIZE_BYTES.
    """
    large_values = ["A" * 1_000 for _ in range(settings.DISPLAY_MAX_ROWS)]

    df = pd.DataFrame()
    for i in range(settings.DISPLAY_MAX_COLUMNS):
        df[f"col_{i}"] = large_values
    return df


@pytest.fixture
def sample_long_dataframe() -> pd.DataFrame:
    num_rows = settings.DISPLAY_MAX_ROWS + 10
    return pd.DataFrame(np.random.rand(num_rows, 1))


@pytest.fixture
def sample_wide_dataframe() -> pd.DataFrame:
    num_cols = settings.DISPLAY_MAX_COLUMNS + 10
    return pd.DataFrame(np.random.rand(1, num_cols))


@pytest.fixture
def sample_long_wide_dataframe() -> pd.DataFrame:
    num_rows = settings.DISPLAY_MAX_ROWS + 10
    num_cols = settings.DISPLAY_MAX_COLUMNS + 10
    return pd.DataFrame(np.random.rand(num_rows, num_cols))


@pytest.fixture
def sample_dex_date_filter(sample_random_dataframe: pd.DataFrame) -> dict:
    return {
        "column": "datetime_column",
        "type": "DATE_FILTER",
        "predicate": "between",
        "start": sample_random_dataframe.datetime_column.min(),
        "end": sample_random_dataframe.datetime_column.max(),
    }


@pytest.fixture
def sample_dex_groupby_date_filter(sample_random_dataframe: pd.DataFrame) -> dict:
    return {
        "column": "datetime_column, min",
        "type": "DATE_FILTER",
        "predicate": "between",
        "start": sample_random_dataframe.datetime_column.min(),
        "end": sample_random_dataframe.datetime_column.max(),
    }


@pytest.fixture
def sample_dex_metric_filter(sample_random_dataframe: pd.DataFrame) -> dict:
    return {
        "column": "float_column",
        "type": "METRIC_FILTER",
        "predicate": "between",
        "value": [
            sample_random_dataframe.float_column.min(),
            sample_random_dataframe.float_column.max(),
        ],
    }


@pytest.fixture
def sample_dex_groupby_metric_filter(sample_random_dataframe: pd.DataFrame) -> dict:
    return {
        "column": "float_column, min",
        "type": "METRIC_FILTER",
        "predicate": "between",
        "value": [
            sample_random_dataframe.float_column.min(),
            sample_random_dataframe.float_column.max(),
        ],
    }


@pytest.fixture
def sample_dex_dimension_filter(sample_random_dataframe: pd.DataFrame) -> dict:
    return {
        "column": "keyword_column",
        "type": "DIMENSION_FILTER",
        "predicate": "in",
        "value": sample_random_dataframe.keyword_column.sample().values.tolist(),
    }


@pytest.fixture
def sample_dex_filters(
    sample_dex_date_filter: dict,
    sample_dex_metric_filter: dict,
    sample_dex_dimension_filter: dict,
) -> list:
    return DEXFilterSettings(
        filters=[
            sample_dex_date_filter,
            sample_dex_metric_filter,
            sample_dex_dimension_filter,
        ]
    ).filters


@pytest.fixture
def sample_dex_groupby_filters(
    sample_dex_groupby_date_filter: dict,
    sample_dex_groupby_metric_filter: dict,
) -> list:
    return DEXFilterSettings(
        filters=[
            sample_dex_groupby_date_filter,
            sample_dex_groupby_metric_filter,
        ]
    ).filters


@pytest.fixture
def sample_dxdataframe(
    get_ipython: TerminalInteractiveShell,
    sample_random_dataframe: pd.DataFrame,
) -> DXDataFrame:
    return DXDataFrame(
        df=sample_random_dataframe,
        ipython_shell=get_ipython,
    )
