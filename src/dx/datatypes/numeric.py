import random
from decimal import Decimal

import numpy as np
import pandas as pd
import structlog

logger = structlog.get_logger(__name__)


### Generator helper functions ###
def generate_integer_series(
    num_rows: int, value_min: int = -100, value_max: int = 100
) -> pd.Series:
    return pd.Series([np.random.randint(value_min, value_max) for _ in range(num_rows)])


def generate_float_series(num_rows: int, value_min: int = 0, value_max: int = 0) -> pd.Series:
    return pd.Series(
        [random.randint(value_min, value_max) + np.random.rand() for _ in range(num_rows)]
    )


def generate_decimal_series(num_rows: int, value_min: int = 0, value_max: int = 0) -> pd.Series:
    return generate_float_series(num_rows, value_min, value_max).apply(lambda x: Decimal(x))


def generate_complex_number_series(num_rows: int) -> pd.Series:
    return pd.Series(
        [complex(real=np.random.rand(), imag=np.random.rand()) for _ in range(num_rows)]
    )


### Handler helper functions ###
def handle_complex_number_series(s: pd.Series) -> pd.Series:
    types = (complex, np.complex)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has complex numbers; converting to real/imag string")
        s = s.apply(lambda x: f"{x.real}+{x.imag}j" if isinstance(x, types) else x)
    return s


def handle_decimal_series(s: pd.Series) -> pd.Series:
    types = (Decimal,)
    if any(isinstance(v, types) for v in s.dropna().head().values):
        logger.debug(f"series `{s.name}` has Decimals; converting to float")
        s = s.astype(float)
    return s
