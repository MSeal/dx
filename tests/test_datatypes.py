"""
Tests to ensure various data types can be sent functions to
- build the table schema and payload/metadata body for each display formatter
- hash the dataframe for tracking
- write to the database for tracking/filtering
"""
from datetime import datetime

import duckdb
import numpy as np
import pandas as pd
import pytest
from pandas.io.json import build_table_schema
from pandas.util import hash_pandas_object

from dx.datatypes import date_time, geometry, main, misc, numeric, text
from dx.datatypes.main import (
    DX_DATATYPES,
    SORTED_DX_DATATYPES,
    quick_random_dataframe,
    random_dataframe,
)
from dx.formatters.main import generate_body
from dx.settings import settings_context
from dx.utils.formatting import clean_column_values
from dx.utils.tracking import generate_df_hash


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


@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_generate_body(dtype: str, display_mode: str):
    """
    Test that we've correctly handled data types before building the schema and metadata for
    the DXDisplayFormatter.
    """
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(**params)
    try:
        with settings_context(display_mode=display_mode):
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
    DEV: Test which data types pass/fail when registered directly to duckdb.
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
    Test that we've correctly handled data types before storing in duckdb.
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


class TestDataFrameGeneration:
    """Basic testing to make sure our dataframe generation provides data with default arguments."""

    @pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
    def test_df_generator(self, dtype: str, num_rows: int = 5):
        params = {dt: False for dt in SORTED_DX_DATATYPES}
        params[dtype] = True
        df = random_dataframe(num_rows=num_rows, **params)
        assert len(df) == num_rows
        assert isinstance(df[dtype], pd.Series)
        assert df[dtype].notnull().all()

    def test_random_dataframe_has_default_data(self, num_rows: int = 5):
        df = random_dataframe(num_rows=num_rows)
        assert len(df) == num_rows
        default_enabled_columns = [column for column, enabled in DX_DATATYPES.items() if enabled]
        assert len(df.columns) == len(default_enabled_columns)
        for col in default_enabled_columns:
            # if this fails, that means something was added to DX_DATATYPES that doesn't match
            # the default arguments of random_dataframe()
            assert col in df.columns
            assert df[col].notnull().all()

    def test_quick_random_dataframe_has_default_data(self):
        df = quick_random_dataframe()
        assert df.shape[0] >= 1
        assert df.shape[1] >= 1
        for col in df.columns:
            assert df[col].notnull().all()


class TestDatatypeHandling:
    def test_integer_series_left_alone(self):
        series = numeric.generate_integer_series(5)
        series = clean_column_values(series)
        assert series.dtype == "int64"
        assert isinstance(
            series.values[0], (int, np.int64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_float_series_left_alone(self):
        series = numeric.generate_float_series(5)
        series = clean_column_values(series)
        assert series.dtype == "float64"
        assert isinstance(
            series.values[0], (float, np.float64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_boolean_series_left_alone(self):
        series = misc.generate_boolean_series(5)
        series = clean_column_values(series)
        assert series.dtype == "bool"
        assert isinstance(
            series.values[0], (bool, np.bool_)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_dtype_series_converted(self):
        series = misc.generate_dtype_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_decimal_series_converted(self):
        series = numeric.generate_decimal_series(5)
        series = clean_column_values(series)
        assert series.dtype == "float64"
        assert isinstance(
            series.values[0], (float, np.float64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_datetime_series_left_alone(self):
        series = date_time.generate_datetime_series(5)
        series = clean_column_values(series)
        assert series.dtype == "datetime64[ns]"
        assert isinstance(
            series.values[0], (datetime, np.datetime64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_datetimetz_series_converted(self):
        series = date_time.generate_datetimetz_series(5)
        series = clean_column_values(series)
        assert str(series.dtype).startswith("datetime64[ns, ")
        assert isinstance(
            series.values[0], (datetime, np.datetime64)
        ), f"cleaned series value is {type(series.values[0])}"
        # this is the most important part to check;
        # if this fails, build_table_schema() will fail
        assert hasattr(series.dtype.tz, "zone")

    def test_date_series_converted(self):
        # datetime.date values are converted to pd.Timestamp
        series = date_time.generate_date_series(5)
        series = clean_column_values(series)
        assert series.dtype == "datetime64[ns]"
        assert isinstance(
            series.values[0], (datetime, np.datetime64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_time_series_converted(self):
        # datetime.time values are converted to strings
        series = date_time.generate_time_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_timedelta_series_converted(self):
        # time delta values are converted to floats (total seconds)
        series = date_time.generate_time_delta_series(5)
        series = clean_column_values(series)
        assert series.dtype == "float64"
        assert isinstance(
            series.values[0], (float, np.float64)
        ), f"cleaned series value is {type(series.values[0])}"

    def test_time_period_series_converted(self):
        series = date_time.generate_time_period_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_time_interval_series_converted(self):
        series = date_time.generate_time_interval_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_text_series_left_alone(self):
        series = text.generate_text_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_keyword_series_left_alone(self):
        series = text.generate_keyword_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_dict_series_converted(self):
        # dictionary values are JSON-stringifed
        series = misc.generate_dict_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_list_series_converted(self):
        # sequence values are cast as strings
        series = misc.generate_list_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_nested_tabular_series_converted(self):
        # lists of dictionaries are JSON-stringified
        series = main.generate_nested_tabular_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_latlon_point_series_converted(self):
        # latlon point values are converted to GeoJSON strings
        series = geometry.generate_latlon_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_filled_geojson_series_converted(self):
        # shapely.geometry values are converted to GeoJSON strings
        # by handle_geometry_series()
        series = geometry.generate_filled_geojson_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_exterior_bounds_geojson_series_converted(self):
        # shapely.geometry exterior values are converted to GeoJSON strings
        # by handle_geometry_series()
        series = geometry.generate_exterior_bounds_geojson_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_bytes_series_converted(self):
        # bytes values are converted to strings
        series = misc.generate_bytes_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_ipv4_address_series_converted(self):
        # IPv4Address values are converted to strings
        series = misc.generate_ipv4_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"

    def test_ipv6_address_series_converted(self):
        # IPv6Address values are converted to strings
        series = misc.generate_ipv6_series(5)
        series = clean_column_values(series)
        assert series.dtype == "object"
        assert isinstance(
            series.values[0], str
        ), f"cleaned series value is {type(series.values[0])}"
