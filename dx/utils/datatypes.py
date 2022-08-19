import ipaddress
import random
import string

import numpy as np
import pandas as pd
import structlog

from dx.utils import date_time, geometry

try:
    from faker import Faker

    fake = Faker()
    FAKER_INSTALLED = True
except ImportError:
    FAKER_INSTALLED = False


logger = structlog.get_logger(__name__)


def handle_dtype_series(s: pd.Series):
    """
    Casts dtypes as strings.
    """
    types = (type, np.dtype)
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has types; converting to strings")
        s = s.astype(str)
    return s


def handle_interval_series(s: pd.Series) -> pd.Series:
    types = (pd.Interval)
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has intervals; converting to left/right")
        s = s.apply(lambda x: [x.left, x.right] if isinstance(x, types) else x)
    return s


def to_dataframe(obj) -> pd.DataFrame:
    """
    Converts an object to a pandas dataframe.
    """
    logger.debug(f"converting {type(obj)} to pd.DataFrame")
    # TODO: support custom converters
    df = pd.DataFrame(obj)
    return df


def quick_random_dataframe(
    num_rows: int = 5,
    num_cols: int = 2,
    dtype: str = "float",
    factor: float = 1.0,
) -> pd.DataFrame:
    """
    Convenience function wrapping `pd.DataFrame(np.random.rand( num_rows, num_columns ))`
    to create a dataframe of random 0.0-1.0 values.
    """
    data = np.random.rand(num_rows, num_cols) * factor
    df = pd.DataFrame(data)
    return df.astype(dtype, errors="ignore")


def generate_integer_series(num_rows: int) -> pd.Series:
    return pd.Series([np.random.randint(-100, 100) for _ in range(num_rows)])


def generate_float_series(num_rows: int) -> pd.Series:
    return pd.Series([np.random.rand() for _ in range(num_rows)])


def generate_complex_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [complex(real=np.random.rand(), imag=np.random.rand()) for _ in range(num_rows)]
    )


def generate_text_series(num_rows: int) -> pd.Series:
    if not FAKER_INSTALLED:
        logger.warning("faker is not installed, skipping text_column")
        return np.nan

    return pd.Series([fake.text() for _ in range(num_rows)])


def generate_keyword_series(num_rows: int, num_letters: int = 2) -> pd.Series:
    return pd.Series(
        ["".join(random.sample(string.ascii_uppercase, num_letters)) for _ in range(num_rows)]
    )


def generate_dict_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            {
                "nested_property": random.choice(["apple", "banana", "orange", "pear"]),
                "nested_other_property": random.randint(0, 10),
                "nested_bool": random.choice([True, False]),
            }
            for _ in range(num_rows)
        ]
    )


def generate_list_series(num_rows: int) -> pd.Series:
    return pd.Series([[random.randint(0, 5) for _ in range(5)] for _ in range(num_rows)])


def generate_bytes_series(num_rows: int, n_bytes: int = 10) -> pd.Series:
    return pd.Series([np.random.bytes(n_bytes) for _ in range(num_rows)])


def generate_nested_tabular_series(num_rows: int, num_nested_rows: int = 5, **kwargs) -> pd.Series:
    return pd.Series(
        [
            random_dataframe(num_rows=num_nested_rows, **kwargs).to_dict("records")
            for _ in range(num_rows)
        ]
    )


def generate_ipv4_series(num_rows: int) -> pd.Series:
    def random_ipv4():
        address_str = ".".join(str(random.randint(0, 255)) for _ in range(4))
        return ipaddress.ip_address(address_str)

    return pd.Series([random_ipv4() for _ in range(num_rows)])


def generate_ipv6_series(num_rows: int) -> pd.Series:
    def random_ipv6():
        address_str = ":".join(str(random.randint(0, 65_535)) for _ in range(8))
        return ipaddress.ip_address(address_str)

    return pd.Series([random_ipv6() for _ in range(num_rows)])


def random_dataframe(
    num_rows: int = 5,
    integer_column: bool = True,
    float_column: bool = True,
    datetime_column: bool = True,
    time_delta_column: bool = True,
    time_period_column: bool = False,
    time_interval_column: bool = False,
    text_column: bool = False,
    keyword_column: bool = True,
    dict_column: bool = False,
    list_column: bool = False,
    nested_tabular_column: bool = False,
    latlon_point_column: bool = False,
    filled_geojson_column: bool = False,
    exterior_geojson_column: bool = False,
    bytes_column: bool = False,
    ipv4_address_column: bool = False,
    ipv6_address_column: bool = False,
    complex_number_column: bool = False,
):  # noqa: C901
    df = pd.DataFrame(index=list(range(num_rows)))

    # numeric columns
    if integer_column:
        df["int_col"] = generate_integer_series(num_rows)

    if float_column:
        df["float_col"] = generate_float_series(num_rows)

    if complex_number_column:
        df["complex_num_col"] = generate_complex_series(num_rows)

    # date/time columns
    if datetime_column:
        df["datetime_col"] = date_time.generate_datetime_series(num_rows)

    if time_delta_column:
        df["time_delta_col"] = date_time.generate_time_delta_series(num_rows)

    if time_period_column:
        df["time_period_col"] = date_time.generate_time_period_series(num_rows)

    if time_interval_column:
        df["time_interval_col"] = date_time.generate_time_interval_series(num_rows)

    # string columns
    if text_column:
        df["text_col"] = generate_text_series(num_rows)

    if keyword_column:
        df["keyword_col"] = generate_keyword_series(num_rows)

    # container columns
    if dict_column:
        df["dict_col"] = generate_dict_series(num_rows)

    if list_column:
        df["list_col"] = generate_list_series(num_rows)

    if nested_tabular_column:
        df["nested_col"] = generate_nested_tabular_series(
            num_rows,
            float_column=True,
            keyword_column=True,
        )

    # geopandas/shapely columns
    if latlon_point_column:
        df["latlon_col"] = geometry.generate_latlon_series(num_rows)

    if filled_geojson_column:
        df["geojson_filled_buffer_col"] = geometry.generate_filled_geojson_series(num_rows)

    if exterior_geojson_column:
        df["geojson_exterior_bounds_col"] = geometry.generate_exterior_bounds_geojson_series(
            num_rows
        )

    # extras
    if bytes_column:
        df["bytes_col"] = generate_bytes_series(num_rows)

    if ipv4_address_column:
        df["ipv4_col"] = generate_ipv4_series(num_rows)

    if ipv6_address_column:
        df["ipv6_col"] = generate_ipv6_series(num_rows)

    return df
