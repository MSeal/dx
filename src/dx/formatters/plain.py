import warnings
from functools import lru_cache
from typing import Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pydantic import Field

from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER
from dx.settings import get_settings
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger(__name__)
settings = get_settings()

warnings.filterwarnings("ignore")


class PandasSettings(BaseSettings):
    # "plain" (pandas) display mode
    PANDAS_DISPLAY_MAX_ROWS: int = 60
    PANDAS_DISPLAY_MAX_COLUMNS: int = 20
    PANDAS_MAX_STRING_LENGTH: int = 50
    PANDAS_HTML_TABLE_SCHEMA: bool = Field(False, frozen=True)
    PANDAS_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", frozen=True)
    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = SettingsConfigDict(validate_assignment=True, json_encoders={type: lambda t: str(t)})


@lru_cache
def get_pandas_settings():
    return PandasSettings()


pandas_settings = get_pandas_settings()


def reset(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Resets all nteract/Noteable options, reverting to the default
    pandas display options and IPython display formatter.
    """
    if get_ipython() is None and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "plain"

    settings.DISPLAY_MAX_COLUMNS = pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS
    settings.DISPLAY_MAX_ROWS = pandas_settings.PANDAS_DISPLAY_MAX_ROWS
    settings.MEDIA_TYPE = pandas_settings.PANDAS_MEDIA_TYPE

    pd.set_option("display.max_columns", pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS)
    pd.set_option("display.max_rows", pandas_settings.PANDAS_DISPLAY_MAX_ROWS)
    pd.set_option("display.max_colwidth", pandas_settings.PANDAS_MAX_STRING_LENGTH)

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER
