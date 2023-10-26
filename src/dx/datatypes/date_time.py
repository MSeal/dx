import datetime

import numpy as np
import pandas as pd
import structlog

from dx.settings import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)


def generate_datetime_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `datetime.datetime` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_pydatetime()
            for _ in range(num_rows)
        ]
    )


def generate_datetimetz_series(num_rows: int, timezone_source: str = "datetime") -> pd.Series:
    """
    Generate a series of random `datetime.datetime` values with `datetime.timezone` information.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    # by default, pandas will use pytz for timezone information,
    # but for testing rendering compatibility, we want to make sure
    # we can handle datetime.timezone as well
    tz = datetime.timezone.utc
    if timezone_source == "pytz":
        tz = "UTC"

    return pd.Series(
        [
            (pd.Timestamp("now", tz=tz) + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours"))
            for _ in range(num_rows)
        ]
    )


def generate_date_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `datetime.date` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [
            (pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")).date()
            for _ in range(num_rows)
        ]
    )


def generate_time_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `datetime.time` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [
            (pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")).time()
            for _ in range(num_rows)
        ]
    )


def generate_time_period_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `pd.Period` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_period(freq="W")
            for _ in range(num_rows)
        ]
    )


def generate_time_interval_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `pd.Interval` values with `pd.Timestamp` left/right values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [
            pd.Interval(
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 0)} hours"),
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(0, 1000)} hours"),
            )
            for _ in range(num_rows)
        ]
    )


def generate_time_delta_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random `pd.Timedelta` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    return pd.Series(
        [pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours") for _ in range(num_rows)]
    )


def handle_time_period_series(s: pd.Series) -> pd.Series:
    types = (pd.Period, pd.PeriodIndex)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has pd.Period values; converting to string")
        s = s.apply(lambda x: [x.start_time, x.end_time] if isinstance(x, types) else x)
    return s


def handle_time_delta_series(s: pd.Series) -> pd.Series:
    types = (
        datetime.timedelta,
        np.timedelta64,
        pd.Timedelta,
    )
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has pd.TimeDelta values; converting to total seconds")
        s = s.apply(lambda x: x.total_seconds() if isinstance(x, types) else x)
    return s


def handle_datetime_series(s: pd.Series) -> pd.Series:
    types = (datetime.date, datetime.datetime, np.datetime64)

    sample_rows = s.dropna().head()
    # in the event we don't have a `datetime64[ns]` dtype (i.e. `object` dtype), we need to check if
    # any of the values have tzinfo property anyway. this might happen as a result of different
    # datetime structures being used in the same series
    has_tzinfo = sample_rows.apply(lambda x: hasattr(x, "tzinfo"))
    if any(isinstance(v, types) for v in sample_rows.values):
        logger.debug(
            f"series `{s.name}` has datetime values; converting with pd.to_datetime()",
            utc=has_tzinfo.any(),
        )
        s = pd.to_datetime(s, utc=has_tzinfo.any())
    return s
