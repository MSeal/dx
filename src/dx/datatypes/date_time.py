import datetime

import numpy as np
import pandas as pd
import structlog

from dx.settings import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)


def generate_datetime_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_pydatetime()
            for _ in range(num_rows)
        ]
    )


def generate_date_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")).date()
            for _ in range(num_rows)
        ]
    )


def generate_time_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")).time()
            for _ in range(num_rows)
        ]
    )


def generate_time_period_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [
            (
                pd.Timestamp("now") + pd.Timedelta(f"{np.random.randint(-1000, 1000)} hours")
            ).to_period(freq="W")
            for _ in range(num_rows)
        ]
    )


def generate_time_interval_series(num_rows: int) -> pd.Series:
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


def handle_date_series(s: pd.Series) -> pd.Series:
    types = (datetime.date,)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(
            f"series `{s.name}` has datetime.date values; converting with pd.to_datetime()"
        )
        s = pd.to_datetime(s)
    return s


def handle_time_series(s: pd.Series) -> pd.Series:
    types = (datetime.time,)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has datetime.time values; converting to string")
        s = s.astype(str)
    return s


def is_datetime_series(s: pd.Series) -> bool:
    if str(s.dtype) in ("int", "float", "bool", "category", "period", "interval"):
        return False
    if str(s.dtype) in ("datetime64"):
        return True

    try:
        s = pd.to_datetime(s)
        return True
    except Exception as e:
        logger.debug(f"series `{s.name}` is not a datetime series: {e}")
        return False
