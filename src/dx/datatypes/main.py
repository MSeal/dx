import numpy as np
import pandas as pd
import structlog

from dx.datatypes import date_time, geometry, misc, numeric, text

logger = structlog.get_logger(__name__)

# this is primarily used for testing to match the optional
# data types used for random dataframe generation,
# and should match the keyword arguments available in `random_dataframe()``
DX_DATATYPES = {
    "dtype_column": True,
    "integer_column": True,
    "float_column": True,
    "bool_column": True,
    "decimal_column": False,
    "datetime_column": True,
    "datetimetz_column": False,
    "date_column": False,
    "time_column": False,
    "time_delta_column": False,
    "time_period_column": False,
    "time_interval_column": False,
    "text_column": False,
    "keyword_column": True,
    "dict_column": False,
    "list_column": False,
    "nested_tabular_column": False,
    "latlon_point_column": False,
    "filled_geojson_column": False,
    "exterior_geojson_column": False,
    "bytes_column": True,
    "ipv4_address_column": False,
    "ipv6_address_column": False,
    "complex_number_column": False,
    "uuid4_column": False,
}
# specifically used for pytest.mark.parametrize ordering
SORTED_DX_DATATYPES = sorted(list(DX_DATATYPES.keys()))


def quick_random_dataframe(
    num_rows: int = 5,
    num_cols: int = 2,
    dtype: str = "float",
    factor: float = 1.0,
) -> pd.DataFrame:
    """
    Convenience function wrapping `pd.DataFrame(np.random.rand( num_rows, num_columns ))`
    to create a dataframe of random 0.0-1.0 values.

    Parameters
    ----------
    num_rows : int
        Number of rows to generate
    num_cols : int
        Number of columns to generate
    dtype : str
        Data type to use for the generated dataframe values.
    factor : float
        Factor to multiply the generated values by.
    """
    data = np.random.rand(num_rows, num_cols) * factor
    df = pd.DataFrame(data)
    return df.astype(dtype, errors="ignore")


def random_dataframe(
    num_rows: int = 5,
    dtype_column: bool = True,
    integer_column: bool = True,
    float_column: bool = True,
    bool_column: bool = True,
    decimal_column: bool = False,
    datetime_column: bool = True,
    datetimetz_column: bool = False,
    date_column: bool = False,
    time_column: bool = False,
    time_delta_column: bool = False,
    time_period_column: bool = False,
    time_interval_column: bool = False,
    text_column: bool = False,
    keyword_column: bool = True,
    dict_column: bool = False,
    list_column: bool = False,
    nested_tabular_column: bool = False,
    lat_float_column: bool = False,
    lon_float_column: bool = False,
    latlon_point_column: bool = False,
    filled_geojson_column: bool = False,
    exterior_geojson_column: bool = False,
    bytes_column: bool = True,
    ipv4_address_column: bool = False,
    ipv6_address_column: bool = False,
    complex_number_column: bool = False,
    uuid4_column: bool = False,
):  # noqa: C901
    """
    Convenience function to generate a dataframe of `num_rows` length
    with randomly-generated values of mixed data types.

    Parameters
    ----------
    num_rows : int
        Number of rows to generate
    dtype_column : bool
        Whether to include a column of `type` values
    integer_column : bool
        Whether to include a column of `integer` values
    float_column : bool
        Whether to include a column of `float` values
    bool_column : bool
        Whether to include a column of `bool` values
    decimal_column : bool
        Whether to include a column of `decimal.Decimal` values
    datetime_column : bool
        Whether to include a column of `datetime.datetime` values
    datetimetz_column : bool
        Whether to include a column of `datetime.datetime` values with timezones
    date_column : bool
        Whether to include a column of `datetime.date` values
    time_column : bool
        Whether to include a column of `datetime.time` values
    time_delta_column : bool
        Whether to include a column of `pd.Timedelta` values
    time_period_column : bool
        Whether to include a column of `pd.Period` values
    time_interval_column : bool
        Whether to include a column of `pd.Interval` values
    text_column : bool
        Whether to include a column of long `str` values using `faker`
    keyword_column : bool
        Whether to include a column of short `str` values
    dict_column : bool
        Whether to include a column of `dict` values
    list_column : bool
        Whether to include a column of `list` values
    nested_tabular_column : bool
        Whether to include a column of `list` values with nested dictionaries
    lat_float_column : bool
        Whether to include a column of `float` values representing latitudes
    lon_float_column : bool
        Whether to include a column of `float` values representing longitudes
    latlon_point_column : bool
        Whether to include a `geopandas.GeoSeries` of `shapely.geometry.Point` values (requires `geopandas` to be installed)
    filled_geojson_column : bool
        Whether to include a `geopandas.GeoSeries` of circular `shapely.geometry.Polygon` values (requires `geopandas` to be installed)
    exterior_geojson_column : bool
        Whether to include a `geopandas.GeoSeries` of rectangular `shapely.geometry.LineString` values (requires `geopandas` to be installed)
    bytes_column : bool
        Whether to include a column of `bytes` values
    ipv4_address_column : bool
        Whether to include a column of `ipaddress.IPv4Address` values
    ipv6_address_column : bool
        Whether to include a column of `ipaddress.IPv6Address` values
    complex_number_column : bool
        Whether to include a column of `complex` values
    uuid4_column : bool
        Whether to include a column of `uuid.UUID` values
    """
    df = pd.DataFrame(index=list(range(num_rows)))

    if dtype_column:
        df["dtype_column"] = misc.generate_dtype_series(num_rows)

    if bool_column:
        df["bool_column"] = misc.generate_boolean_series(num_rows)

    # numeric columns
    if integer_column:
        df["integer_column"] = numeric.generate_integer_series(num_rows)

    if float_column:
        df["float_column"] = numeric.generate_float_series(num_rows)

    if decimal_column:
        df["decimal_column"] = numeric.generate_decimal_series(num_rows)

    if complex_number_column:
        df["complex_number_column"] = numeric.generate_complex_number_series(num_rows)

    # date/time columns
    if datetime_column:
        df["datetime_column"] = date_time.generate_datetime_series(num_rows)

    if datetimetz_column:
        df["datetimetz_column"] = date_time.generate_datetimetz_series(num_rows)

    if date_column:
        df["date_column"] = date_time.generate_date_series(num_rows)

    if time_column:
        df["time_column"] = date_time.generate_time_series(num_rows)

    if time_delta_column:
        df["time_delta_column"] = date_time.generate_time_delta_series(num_rows)

    if time_period_column:
        df["time_period_column"] = date_time.generate_time_period_series(num_rows)

    if time_interval_column:
        df["time_interval_column"] = date_time.generate_time_interval_series(num_rows)

    # string columns
    if text_column:
        df["text_column"] = text.generate_text_series(num_rows)

    if keyword_column:
        df["keyword_column"] = text.generate_keyword_series(num_rows)

    # container columns
    if dict_column:
        df["dict_column"] = misc.generate_dict_series(num_rows)

    if list_column:
        df["list_column"] = misc.generate_list_series(num_rows)

    if nested_tabular_column:
        df["nested_tabular_column"] = generate_nested_tabular_series(
            num_rows,
            float_column=True,
            keyword_column=True,
        )

    # geopandas/shapely columns
    if lat_float_column:
        df["lat_float_column"] = geometry.generate_lat_float_series(num_rows)

    if lon_float_column:
        df["lon_float_column"] = geometry.generate_lon_float_series(num_rows)

    if latlon_point_column:
        df["latlon_point_column"] = geometry.generate_latlon_series(num_rows)

    if filled_geojson_column:
        df["filled_geojson_column"] = geometry.generate_filled_geojson_series(num_rows)

    if exterior_geojson_column:
        df["exterior_geojson_column"] = geometry.generate_exterior_bounds_geojson_series(num_rows)

    # extras
    if bytes_column:
        df["bytes_column"] = misc.generate_bytes_series(num_rows)

    if ipv4_address_column:
        df["ipv4_address_column"] = misc.generate_ipv4_series(num_rows)

    if ipv6_address_column:
        df["ipv6_address_column"] = misc.generate_ipv6_series(num_rows)

    if uuid4_column:
        df["uuid4_column"] = misc.generate_uuid4_series(num_rows)

    return df


# not adding this to datatypes/misc.py due to circular import
def generate_nested_tabular_series(num_rows: int, num_nested_rows: int = 5, **kwargs) -> pd.Series:
    """
    Generate a series of random lists of nested dictionaries. (Uses `random_dataframe()`)

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    num_nested_rows: int
        Number of rows to generate for each nested dictionary
    """
    return pd.Series(
        [
            random_dataframe(num_rows=num_nested_rows, **kwargs).to_dict("records")
            for _ in range(num_rows)
        ]
    )
