import random
import string

import numpy as np
import pandas as pd
import structlog

logger = structlog.get_logger(__name__)


def generate_text_series(num_rows: int) -> pd.Series:
    """
    Generate a series of random long `str` values. (Requires `faker` to be installed)

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    """
    try:
        from faker import Faker

    except ImportError:
        logger.warning("faker is not installed, skipping text_column")
        return np.nan

    faker_instance = Faker()
    return pd.Series([faker_instance.text() for _ in range(num_rows)])


def generate_keyword_series(num_rows: int, num_letters: int = 2) -> pd.Series:
    """
    Generate a series of random short `str` values.

    Parameters
    ----------
    num_rows: int
        Number of rows to generate
    num_letters: int
        Number of letters to use in each keyword
    """
    return pd.Series(
        ["".join(random.sample(string.ascii_uppercase, num_letters)) for _ in range(num_rows)]
    )
