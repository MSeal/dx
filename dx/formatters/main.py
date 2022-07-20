import warnings
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.settings import settings

warnings.filterwarnings("ignore")


DISPLAY_ID_TO_DATAFRAME = {}


def reset(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Resets all nteract/Noteable options,
    reverting to the default pandas display options.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "default"

    pd.set_option("display.max_rows", settings.PANDAS_DISPLAY_MAX_ROWS)
    pd.set_option("html.table_schema", settings.PANDAS_HTML_TABLE_SCHEMA)

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER
