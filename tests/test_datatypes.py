"""
Tests to ensure various data types can be sent functions to
- build the table schema and payload/metadata body for each display formatter
- hash the dataframe for tracking
- write to the database for tracking/filtering
"""

import duckdb
import pandas as pd
import pytest
from pandas.io.json import build_table_schema
from pandas.util import hash_pandas_object

from dx.formatters.main import generate_body
from dx.settings import settings_context
from dx.utils.datatypes import (
    DX_DATATYPES,
    SORTED_DX_DATATYPES,
    groupby_series_index_name,
    quick_random_dataframe,
    random_dataframe,
    to_dataframe,
)
from dx.utils.formatting import clean_column_values
from dx.utils.tracking import generate_df_hash


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_df_generator(dtype: str, num_rows: int = 5):
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(num_rows=num_rows, **params)
    assert len(df) == num_rows
    assert isinstance(df[dtype], pd.Series)
    assert df[dtype].notnull().all()


def test_random_dataframe_has_default_data(num_rows: int = 5):
    df = random_dataframe(num_rows=num_rows)
    assert len(df) == num_rows
    default_enabled_columns = [column for column, enabled in DX_DATATYPES.items() if enabled]
    assert len(df.columns) == len(default_enabled_columns)
    for col in default_enabled_columns:
        assert col in df.columns
        assert df[col].notnull().all()


def test_quick_random_dataframe_has_default_data():
    df = quick_random_dataframe()
    assert df.shape[0] >= 1
    assert df.shape[1] >= 1
    for col in df.columns:
        assert df[col].notnull().all()


@pytest.mark.xfail(reason="only for dev")
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_data_types_with_build_table_schema(dtype: str):
    """
    DEV: Test which data types pass/fail when passed directly through build_table_schema().
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        schema = build_table_schema(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(schema, dict)


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_generate_simple_body(dtype: str):
    """
    Test that we've correctly handled data types before building the schema and metadata for
    the DXDisplayFormatter.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        with settings_context(display_mode="simple"):
            payload = generate_body(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(payload, dict)


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_generate_enhanced_body(dtype: str):
    """
    Test that we've correctly handled data types before building the schema and metadata for
    the DXDisplayFormatter.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        with settings_context(display_mode="enhanced"):
            payload = generate_body(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(payload, dict)


@pytest.mark.xfail(reason="only for dev")
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_hash_pandas_object(dtype: str):
    """
    DEV: Test which data types pass/fail when passed directly through hash_pandas_object().
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        hash_series = hash_pandas_object(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(hash_series, pd.Series)


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_generate_df_hash(dtype: str):
    """
    Test that we've correctly handled data types before creating a hash of a dataframe.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    for col in df.columns:
        df[col] = clean_column_values(df[col])
    try:
        hash_str = generate_df_hash(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(hash_str, str)


@pytest.mark.xfail(reason="only for dev")
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_to_sql(dtype: str, sample_db_connection: duckdb.DuckDBPyConnection):
    """
    DEV: Test which data types pass/fail when passed directly through .to_sql()
    with the sqlalchemy engine.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True

    df = random_dataframe(**params)

    try:
        sample_db_connection.register(f"{dtype}_test", df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    count_resp = sample_db_connection.execute(f"SELECT COUNT(*) FROM {dtype}_test").fetchone()
    num_rows = count_resp[0]
    assert num_rows == df.shape[0]


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_store_in_db(dtype: str, sample_db_connection: duckdb.DuckDBPyConnection):
    """
    Test that we've correctly handled data types before storing in sqlite.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True

    df = random_dataframe(**params)

    for col in df.columns:
        df[col] = clean_column_values(df[col])

    try:
        sample_db_connection.register(f"{dtype}_test", df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    count_resp = sample_db_connection.execute(f"SELECT COUNT(*) FROM {dtype}_test").fetchone()
    num_rows = count_resp[0]
    assert num_rows == df.shape[0]


def test_series_is_converted(sample_random_dataframe: pd.Series):
    """
    Test that a basic conversion from pd.Series to pd.Dataframe
    keeps the original index and uses the Series name as its only column.
    """
    s: pd.Series = sample_random_dataframe.keyword_column
    df = to_dataframe(s)
    assert df.index.equals(s.index)
    assert df.columns[0] == s.name


def test_multiindex_series_left_alone(sample_multiindex_series: pd.Series):
    """
    Test no renaming is done with a MultiIndex pd.Series if their
    name doesn't appear in the MultiIndex names.
    """
    index = sample_multiindex_series.index
    df = to_dataframe(sample_multiindex_series)
    assert df.index.names == index.names
    assert df.columns[0] == sample_multiindex_series.name


def test_groupby_series_resets(sample_groupby_series: pd.Series):
    """
    Test we're resetting the index of a pd.Series created from a groupby
    operation by using the combination of index names.
    """
    index = sample_groupby_series.index
    df = to_dataframe(sample_groupby_series)
    assert df.index.names == index.names
    assert df.columns[0] == groupby_series_index_name(index)
    assert df.columns[0] != sample_groupby_series.name


def test_dataframe_index_left_alone(sample_random_dataframe: pd.DataFrame):
    """
    Ensure we don't alter the structure of a dataframe during
    initial dataframe conversion.
    """
    df = to_dataframe(sample_random_dataframe)
    assert df.index.equals(sample_random_dataframe.index)
    assert df.columns.equals(sample_random_dataframe.columns)


def test_groupby_dataframe_index_left_alone(sample_groupby_dataframe: pd.DataFrame):
    """
    Ensure we don't alter the structure of a dataframe
    with MultiIndexes during initial dataframe conversion.
    """
    df = to_dataframe(sample_groupby_dataframe)
    assert df.index.equals(sample_groupby_dataframe.index)
    assert df.columns.equals(sample_groupby_dataframe.columns)
