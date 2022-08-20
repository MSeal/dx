"""
Tests to ensure various data types can be sent functions to
- build the table schema and payload/metadata body for each display formatter
- hash the dataframe for tracking
- write to sqlite for tracking/filtering
"""

import pandas as pd
import pytest
from pandas.io.json import build_table_schema
from pandas.util import hash_pandas_object

from dx.formatters import dataresource, dx
from dx.utils.datatypes import SORTED_DX_DATATYPES, random_dataframe
from dx.utils.tracking import generate_df_hash, sql_engine, store_in_sqlite


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_df_generator(dtype: str, num_rows: int = 5):
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(num_rows=num_rows, **params)
    assert len(df) == num_rows
    assert isinstance(df[dtype], pd.Series)
    assert df[dtype].notnull().all()


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
def test_generate_dataresource_body(dtype: str):
    """
    Test that we've correctly handled data types before building the schema and metadata for
    the DXDataResourceDisplayFormatter.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        payload, metadata = dataresource.generate_dataresource_body(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(payload, dict)
    assert isinstance(metadata, dict)


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_generate_dx_body(dtype: str):
    """
    Test that we've correctly handled data types before building the schema and metadata for
    the DXDisplayFormatter.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        payload, metadata = dx.generate_dx_body(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(payload, dict)
    assert isinstance(metadata, dict)


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
    try:
        hash_str = generate_df_hash(df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert isinstance(hash_str, str)


@pytest.mark.xfail(reason="only for dev")
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_to_sql(dtype: str):
    """
    DEV: Test which data types pass/fail when passed directly through .to_sql()
    with the sqlalchemy engine.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        with sql_engine.connect() as conn:
            num_rows = df.to_sql("test", conn, if_exists="replace")
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert num_rows == df.shape[0]


@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_store_in_sqlite(dtype: str):
    """
    Test that we've correctly handled data types before storing in sqlite.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        num_rows = store_in_sqlite(f"{dtype}_test", df)
    except Exception as e:
        assert False, f"{dtype} failed with {e}"
    assert num_rows == df.shape[0]


# TODO: test that we can convert back to original datatypes after read_sql?
