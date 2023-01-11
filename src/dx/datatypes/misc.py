import ipaddress
import json
import random
import uuid

import numpy as np
import pandas as pd
import structlog

logger = structlog.get_logger(__name__)


### Generator helper functions ###
def generate_boolean_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `boolean` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series([random.choice([True, False]) for _ in range(num_rows)])


def generate_dtype_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `type` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [random.choice([float, int, str, bool, set, tuple, dict, list]) for _ in range(num_rows)]
    )


def generate_dict_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `dict` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
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
    """
    Generate a series of random `list` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series([[random.randint(0, 5) for _ in range(5)] for _ in range(num_rows)])


def generate_bytes_series(num_rows: int, n_bytes: int = 10) -> pd.Series:
    """
    Generate a series of random `bytes` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    n_bytes: int
        Number of bytes to generate per row
    """
    return pd.Series([np.random.bytes(n_bytes) for _ in range(num_rows)])


def generate_ipv4_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `ipaddress.IPv4Address` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """

    def random_ipv4():
        address_str = ".".join(str(random.randint(0, 255)) for _ in range(4))
        return ipaddress.ip_address(address_str)

    return pd.Series([random_ipv4() for _ in range(num_rows)])


def generate_ipv6_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `ipaddress.IPv6Address` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """

    def random_ipv6():
        address_str = ":".join(
            str(hex(random.randint(0, 65_535))).replace("0x", "") for _ in range(8)
        )
        return ipaddress.ip_address(address_str)

    return pd.Series([random_ipv6() for _ in range(num_rows)])


def generate_uuid4_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `uuid.UUID` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series([uuid.uuid4() for _ in range(num_rows)])


### Handler helper functions ###
def handle_dict_series(s: pd.Series) -> pd.Series:
    types = dict
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has dicts; converting to json string")
        s = s.apply(lambda x: json.dumps(x) if isinstance(x, types) else x)
    return s


def handle_dtype_series(s: pd.Series):
    """
    Casts dtypes as strings.
    """
    types = (type, np.dtype)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has types; converting to strings")
        s = s.astype(str)
    return s


def handle_interval_series(s: pd.Series) -> pd.Series:
    types = pd.Interval
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has intervals; converting to left/right")
        s = s.apply(lambda x: [x.left, x.right] if isinstance(x, types) else x)
    return s


def handle_ip_address_series(s: pd.Series) -> pd.Series:
    types = (ipaddress.IPv4Address, ipaddress.IPv6Address)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has ip addresses; converting to strings")
        s = s.astype(str)
    return s


def handle_sequence_series(s: pd.Series) -> pd.Series:
    types = (list, tuple, set, np.ndarray)
    if is_sequence_series(s):
        logger.debug(f"series `{s.name}` has sequences; converting to comma-separated string")
        s = s.apply(lambda x: ", ".join([str(val) for val in x] if isinstance(x, types) else x))
    return s


def handle_unk_type_series(s: pd.Series) -> pd.Series:
    if not is_json_serializable(s):
        logger.debug(f"series `{s.name}` has non-JSON-serializable types; converting to string")
        s = s.astype(str)
    return s


def handle_uuid_series(s: pd.Series) -> pd.Series:
    if any(isinstance(v, uuid.UUID) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has uuids; converting to strings")
        s = s.astype(str)
    return s


### Type checking helper functions ###
def is_sequence_series(s: pd.Series) -> bool:
    """
    Returns True if the series has any list/tuple/set/array values.
    """
    if str(s.dtype) != "object":
        return False

    if any(isinstance(v, (list, tuple, set, np.ndarray)) for v in s.dropna().head().values):
        return True
    return False


def is_json_serializable(s: pd.Series) -> bool:
    """
    Returns True if the object can be serialized to JSON.
    """
    try:
        _ = json.dumps(s.dropna().head().values.tolist())
        return True
    except (TypeError, OverflowError, UnicodeDecodeError):
        # these are the main serialization errors we expect
        return False
    except ValueError as ve:
        # ...but we may get here if we have a series with duplicate index values
        # "ValueError: Series index must be unique for orient='index'"
        logger.debug(ve)
        return False
