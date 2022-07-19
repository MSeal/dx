import warnings
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.formatters.dataresource import deregister
from dx.formatters.dx import register

warnings.filterwarnings("ignore")

DEFAULT_DISPLAY_MAX_ROWS = 60
DEFAULT_DISPLAY_MAX_COLUMNS = 20
DEFAULT_HTML_TABLE_SCHEMA = False

DISPLAY_MODE = "simple"

DISPLAY_ID_TO_DATAFRAME = {}


def reset(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Resets all nteract/Noteable options,
    reverting to the default pandas display options.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.set_option("html.table_schema", DEFAULT_HTML_TABLE_SCHEMA)
    pd.options.display.max_rows = DEFAULT_DISPLAY_MAX_ROWS
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER


def set_display_mode(mode: str = "simple"):
    """
    Sets the display mode for the IPython formatter in the current session.
    - "default" (vanilla python/pandas display)
    - "simple" (classic simpleTable/DEX display)
    - "enhanced" (GRID display)
    """
    global DISPLAY_MODE
    DISPLAY_MODE = mode

    if mode == "enhanced":
        register()
    elif mode == "simple":
        deregister()
    elif mode == "default":
        reset()
