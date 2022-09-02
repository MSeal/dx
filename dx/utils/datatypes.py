import ipaddress
import json
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


DX_DATATYPES = {
    "dtype_column": True,
    "integer_column": True,
    "float_column": True,
    "datetime_column": True,
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
}
SORTED_DX_DATATYPES = sorted(list(DX_DATATYPES.keys()))


def generate_integer_series(num_rows: int) -> pd.Series:
    return pd.Series([np.random.randint(-100, 100) for _ in range(num_rows)])


def generate_float_series(num_rows: int) -> pd.Series:
    return pd.Series([np.random.rand() for _ in range(num_rows)])


def generate_complex_number_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [complex(real=np.random.rand(), imag=np.random.rand()) for _ in range(num_rows)]
    )


def generate_dtype_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [random.choice([float, int, str, bool, set, tuple, dict, list]) for _ in range(num_rows)]
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
        address_str = ":".join(
            str(hex(random.randint(0, 65_535))).replace("0x", "") for _ in range(8)
        )
        return ipaddress.ip_address(address_str)

    return pd.Series([random_ipv6() for _ in range(num_rows)])


def handle_complex_number_series(s: pd.Series) -> pd.Series:
    types = (complex, np.complex)
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has complex numbers; converting to real/imag string")
        s = s.apply(lambda x: f"{x.real}+{x.imag}j" if isinstance(x, types) else x)
    return s


def handle_dict_series(s: pd.Series) -> pd.Series:
    types = dict
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has dicts; converting to json string")
        s = s.apply(lambda x: json.dumps(x) if isinstance(x, types) else x)
    return s


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
    types = pd.Interval
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has intervals; converting to left/right")
        s = s.apply(lambda x: [x.left, x.right] if isinstance(x, types) else x)
    return s


def handle_ip_address_series(s: pd.Series) -> pd.Series:
    types = (ipaddress.IPv4Address, ipaddress.IPv6Address)
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has ip addresses; converting to strings")
        s = s.astype(str)
    return s


def handle_sequence_series(s: pd.Series) -> pd.Series:
    types = (list, tuple, set, np.ndarray)
    if is_sequence_series(s):
        logger.debug(f"series `{s.name}` has sequences; converting to comma-separated string")
        s = s.apply(lambda x: ", ".join([str(val) for val in x] if isinstance(x, types) else x))
    return s


def is_sequence_series(s: pd.Series) -> bool:
    """
    Returns True if the series has any list/tuple/set/array values.
    """
    if str(s.dtype) != "object":
        return False

    if any(isinstance(v, (list, tuple, set, np.ndarray)) for v in s.values):
        return True
    return False


def handle_unk_type_series(s: pd.Series) -> pd.Series:
    if not is_json_serializable(s):
        logger.debug(f"series `{s.name}` has non-JSON-serializable types; converting to string")
        s = s.astype(str)
    return s


def is_json_serializable(s: pd.Series) -> bool:
    """
    Returns True if the object can be serialized to JSON.
    """
    try:
        s.to_json()
        return True
    except (TypeError, OverflowError, UnicodeDecodeError):
        return False


def has_numeric_strings(s: pd.Series) -> bool:
    if not str(s.dtype) == "object":
        return False
    for v in s.values:
        if str(v).isnumeric() or str(v).isdigit() or str(v).isdecimal():
            return True
    return False


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


def random_dataframe(num_rows: int = 5, **kwargs):  # noqa: C901

    kwargs = kwargs or DX_DATATYPES
    df = pd.DataFrame(index=list(range(num_rows)))

    if kwargs.get("dtype_column"):
        df["dtype_column"] = generate_dtype_series(num_rows)

    # numeric columns
    if kwargs.get("integer_column"):
        df["integer_column"] = generate_integer_series(num_rows)

    if kwargs.get("float_column"):
        df["float_column"] = generate_float_series(num_rows)

    if kwargs.get("complex_number_column"):
        df["complex_number_column"] = generate_complex_number_series(num_rows)

    # date/time columns
    if kwargs.get("datetime_column"):
        df["datetime_column"] = date_time.generate_datetime_series(num_rows)

    if kwargs.get("time_delta_column"):
        df["time_delta_column"] = date_time.generate_time_delta_series(num_rows)

    if kwargs.get("time_period_column"):
        df["time_period_column"] = date_time.generate_time_period_series(num_rows)

    if kwargs.get("time_interval_column"):
        df["time_interval_column"] = date_time.generate_time_interval_series(num_rows)

    # string columns
    if kwargs.get("text_column"):
        df["text_column"] = generate_text_series(num_rows)

    if kwargs.get("keyword_column"):
        df["keyword_column"] = generate_keyword_series(num_rows)

    # container columns
    if kwargs.get("dict_column"):
        df["dict_column"] = generate_dict_series(num_rows)

    if kwargs.get("list_column"):
        df["list_column"] = generate_list_series(num_rows)

    if kwargs.get("nested_tabular_column"):
        df["nested_tabular_column"] = generate_nested_tabular_series(
            num_rows,
            float_column=True,
            keyword_column=True,
        )

    # geopandas/shapely columns
    if kwargs.get("latlon_point_column"):
        df["latlon_point_column"] = geometry.generate_latlon_series(num_rows)

    if kwargs.get("filled_geojson_column"):
        df["filled_geojson_column"] = geometry.generate_filled_geojson_series(num_rows)

    if kwargs.get("exterior_geojson_column"):
        df["exterior_geojson_column"] = geometry.generate_exterior_bounds_geojson_series(num_rows)

    # extras
    if kwargs.get("bytes_column"):
        df["bytes_column"] = generate_bytes_series(num_rows)

    if kwargs.get("ipv4_address_column"):
        df["ipv4_address_column"] = generate_ipv4_series(num_rows)

    if kwargs.get("ipv6_address_column"):
        df["ipv6_address_column"] = generate_ipv6_series(num_rows)

    return df


def to_dataframe(obj) -> pd.DataFrame:
    """
    Converts an object to a pandas dataframe.
    """
    logger.debug(f"converting {type(obj)} to pd.DataFrame")
    # TODO: support custom converters
    df = pd.DataFrame(obj)
    return df
