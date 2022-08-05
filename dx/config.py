import os

from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter

IN_IPYTHON_ENV = get_ipython() is not None

DEFAULT_IPYTHON_DISPLAY_FORMATTER = DisplayFormatter()
if IN_IPYTHON_ENV:
    DEFAULT_IPYTHON_DISPLAY_FORMATTER = get_ipython().display_formatter

# we don't want to require geopandas as a hard dependency
try:
    import geopandas as gpd

    GEOPANDAS_INSTALLED = True
except ImportError:
    GEOPANDAS_INSTALLED = False


def in_noteable_env() -> bool:
    """
    Check if we are running in a Noteable environment.

    FUTURE: this will be used to determine whether IPython formatters
    are automatically updated.
    """
    return "NTBL_USER_ID" in os.environ


def in_nteract_env() -> bool:
    # TODO: handle this?
    return False
