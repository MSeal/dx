import warnings
from functools import lru_cache

import pandas as pd
import structlog
from pydantic import BaseSettings, Field

from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER
from dx.settings import get_settings
from dx.shell import get_ipython_shell

logger = structlog.get_logger(__name__)
settings = get_settings()

warnings.filterwarnings("ignore")


class PandasSettings(BaseSettings):
    # "plain" (pandas) display mode
    PANDAS_DISPLAY_MAX_ROWS: int = 60
    PANDAS_DISPLAY_MAX_COLUMNS: int = 20
    PANDAS_MAX_STRING_LENGTH: int = 50
    PANDAS_HTML_TABLE_SCHEMA: bool = Field(False, allow_mutation=False)
    PANDAS_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", allow_mutation=False)

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_pandas_settings():
    return PandasSettings()


pandas_settings = get_pandas_settings()


def reset() -> None:
    """
    Resets all nteract/Noteable options, reverting to the default
    pandas display options and IPython display formatter.
    """
    settings.DISPLAY_MODE = "plain"

    settings.DISPLAY_MAX_COLUMNS = pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS
    settings.DISPLAY_MAX_ROWS = pandas_settings.PANDAS_DISPLAY_MAX_ROWS
    settings.MEDIA_TYPE = pandas_settings.PANDAS_MEDIA_TYPE

    pd.set_option("display.max_columns", pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS)
    pd.set_option("display.max_rows", pandas_settings.PANDAS_DISPLAY_MAX_ROWS)
    pd.set_option("display.max_colwidth", pandas_settings.PANDAS_MAX_STRING_LENGTH)

    get_ipython_shell().display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER
