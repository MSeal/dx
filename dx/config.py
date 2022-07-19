import os

from IPython import get_ipython

IN_IPYTHON_ENV = get_ipython() is not None

DEFAULT_IPYTHON_DISPLAY_FORMATTER = None
if IN_IPYTHON_ENV:
    DEFAULT_IPYTHON_DISPLAY_FORMATTER = get_ipython().display_formatter


DEFAULT_MAX_SIZE_BYTES = 1 * 1024 * 1024  # default to 1mb


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
