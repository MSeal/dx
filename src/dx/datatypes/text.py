import random
import string

import numpy as np
import pandas as pd
import structlog

try:
    from faker import Faker

    fake = Faker()
    FAKER_INSTALLED = True
except ImportError:
    FAKER_INSTALLED = False


logger = structlog.get_logger(__name__)


def generate_text_series(num_rows: int) -> pd.Series:
    if not FAKER_INSTALLED:
        logger.warning("faker is not installed, skipping text_column")
        return np.nan

    return pd.Series([fake.text() for _ in range(num_rows)])


def generate_keyword_series(num_rows: int, num_letters: int = 2) -> pd.Series:
    return pd.Series(
        ["".join(random.sample(string.ascii_uppercase, num_letters)) for _ in range(num_rows)]
    )
