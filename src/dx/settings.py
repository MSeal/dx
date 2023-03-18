import logging
from contextlib import contextmanager
from functools import lru_cache
from typing import Callable, Dict, Optional, Union

import pandas as pd
import structlog
from pandas import set_option as pandas_set_option
from pydantic import BaseSettings, validator

from dx.dependencies import get_default_renderable_types
from dx.shell import get_ipython_shell
from dx.types.main import DXDisplayMode, DXSamplingMethod

MB = 1024 * 1024

logger = structlog.get_logger(__name__)


class Settings(BaseSettings):
    LOG_LEVEL: Union[int, str] = logging.WARNING

    # IPython.display.JSON payload/metadata during handle_format()
    DEV_MODE: bool = False

    DISPLAY_MAX_ROWS: int = 60
    DISPLAY_MAX_COLUMNS: int = 20
    HTML_TABLE_SCHEMA: bool = False
    MEDIA_TYPE: str = "application/vnd.dataresource+json"

    MAX_RENDER_SIZE_BYTES: int = 100 * MB
    MAX_STRING_LENGTH: int = 50

    RENDERABLE_TYPES: Dict[type, Optional[Union[Callable, str]]] = {}

    # what percentage of the dataset to remove during each sampling
    # in order to get large datasets under MAX_RENDER_SIZE_BYTES
    SAMPLING_FACTOR: float = 0.1

    DISPLAY_MODE: DXDisplayMode = DXDisplayMode.simple

    SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.random
    COLUMN_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.outer
    ROW_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.random
    # TODO: support more than just int type here
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html
    RANDOM_STATE: int = 12_648_430

    RESET_INDEX_VALUES: bool = False

    FLATTEN_INDEX_VALUES: bool = False
    FLATTEN_COLUMN_VALUES: bool = False
    STRINGIFY_INDEX_VALUES: bool = False
    STRINGIFY_COLUMN_VALUES: bool = False

    DATETIME_STRING_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f"

    # controls dataframe variable tracking, hashing, and storing in sqlite
    ENABLE_DATALINK: bool = True
    ENABLE_ASSIGNMENT: bool = True

    NUM_PAST_SAMPLES_TRACKED: int = 3
    DB_LOCATION: str = ":memory:"

    GENERATE_DEX_METADATA: bool = False
    ALLOW_NOTEABLE_ATTRS: bool = True

    @validator("RENDERABLE_TYPES", pre=True, always=True)
    def validate_renderables(cls, vals):
        """Allow passing comma-separated strings or actual types."""
        vals = vals or get_default_renderable_types()
        if isinstance(vals, dict):
            return vals

        # if we don't have a dictionary by now, we should either have
        # a string or a list/set/tuple of strings/types
        if isinstance(vals, str):
            vals = vals.replace(",", "").split()

        valid_vals = {}
        for val in vals:
            if not isinstance(val, type):
                raise ValueError(f"{val} is not a valid type")

            valid_vals[val] = None

        return valid_vals

    @validator("DISPLAY_MAX_COLUMNS", pre=True, always=True)
    def validate_display_max_columns(cls, val):
        if val < 0:
            raise ValueError("DISPLAY_MAX_COLUMNS must be >= 0")
        if val > 50_000:
            raise ValueError("DISPLAY_MAX_COLUMNS must be <= 50000")
        pd.set_option("display.max_columns", val)
        return val

    @validator("DISPLAY_MAX_ROWS", pre=True, always=True)
    def validate_display_max_rows(cls, val):
        if val < 0:
            raise ValueError("DISPLAY_MAX_ROWS must be >= 0")
        pd.set_option("display.max_rows", val)
        return val

    @validator("HTML_TABLE_SCHEMA", pre=True, always=True)
    def validate_html_table_schema(cls, val):
        pd.set_option("html.table_schema", val)
        return val

    @validator("MAX_STRING_LENGTH", pre=True, always=True)
    def validate_max_string_length(cls, val):
        if val < 0:
            raise ValueError("MAX_STRING_LENGTH must be >= 0")
        pd.set_option("display.max_colwidth", val)
        return val

    def get_renderable_types(self):
        return {
            **self.RENDERABLE_TYPES,
            **get_default_renderable_types(),
        }

    class Config:
        validate_assignment = True
        use_enum_values = True


@lru_cache
def get_settings():
    return Settings()


def enable_dev_mode(debug_logs: bool = False) -> None:
    """
    Convenience function to display payload/metadata blobs with `IPython.display.JSON`
    after `handle_format()` is called.

    Parameters
    ----------
    debug_logs: bool
        If True, set log level to DEBUG
    """
    set_option("DEV_MODE", True)
    if debug_logs:
        set_option("LOG_LEVEL", "DEBUG")


def disable_dev_mode() -> None:
    set_option("DEV_MODE", False)
    if get_settings().LOG_LEVEL == "DEBUG":
        set_option("LOG_LEVEL", "WARNING")


def set_display_mode(mode: DXDisplayMode = DXDisplayMode.simple):
    """
    Sets the display mode for the IPython formatter in the current session.
    - "plain" (vanilla python/pandas display)
    - "simple" (classic simpleTable/DEX display)
    - "enhanced" (GRID display)
    """
    # circular imports
    from dx.formatters.enhanced import register
    from dx.formatters.plain import reset
    from dx.formatters.simple import deregister

    get_settings().DISPLAY_MODE = mode

    if str(mode) == DXDisplayMode.enhanced.value:
        register()
    elif str(mode) == DXDisplayMode.simple.value:
        deregister()
    elif str(mode) == DXDisplayMode.plain.value:
        reset()
    else:
        raise ValueError(f"`{mode}` is not a supported display mode")


def set_log_level(level: int):
    logging.getLogger("dx").setLevel(level)


def set_option(key, value) -> None:
    key = str(key).upper()

    settings = get_settings()
    if key in vars(settings):
        setattr(settings, key, value)

        # make sure pandas settings are updated as well for display sizes
        pd_options = {
            "DISPLAY_MAX_ROWS": "display.max_rows",
            "DISPLAY_MAX_COLUMNS": "display.max_columns",
            "HTML_TABLE_SCHEMA": "html.table_schema",
        }
        if key in pd_options:
            logger.debug(f"setting pandas option {pd_options[key]} to {value}")
            pandas_set_option(pd_options[key], value)

        # this may be the most straightforward way to handle
        # IPython display formatter changes being done through
        # settings updates for now, but I don't like it being here
        if key == "DISPLAY_MODE":
            set_display_mode(value)

        if key == "LOG_LEVEL":
            set_log_level(value)

        # allow enabling/disabling comms based on settings
        enable_disable_comms(setting_name=key, enabled=value)

        return
    raise ValueError(f"`{key}` is not a valid setting")


def enable_disable_comms(setting_name: str, enabled: bool) -> None:
    """
    Registers/unregisters a target based on its associated name within Settings.
    For example, the following will unregister the "datalink_resample" comm:
    >>> enable_disable_comms("ENABLE_DATALINK", False)
    And to re-register it:
    >>> enable_disable_comms("ENABLE_DATALINK", True)
    """
    from dx import comms

    comm_setting_targets = {
        "ENABLE_DATALINK": ("datalink_resample", comms.resample.resampler),
        "ENABLE_ASSIGNMENT": ("datalink_assignment", comms.assignment.dataframe_assignment),
    }
    if setting_name not in comm_setting_targets:
        return

    comm_target, comm_callback = comm_setting_targets[setting_name]

    comm_mgr = get_ipython_shell().kernel.comm_manager
    if enabled:
        comm_mgr.register_target(comm_target, comm_callback)
    else:
        comm_mgr.unregister_target(comm_target, comm_callback)


@contextmanager
def settings_context(**option_kwargs):
    settings = get_settings()
    orig_settings = settings.dict()
    option_kwargs = {str(k).upper(): v for k, v in option_kwargs.items()}

    # handle DISPLAY_MODE updates first since it can overwrite other settings
    if display_mode := option_kwargs.pop("DISPLAY_MODE", None):
        set_display_mode(display_mode)

    try:
        for setting, value in option_kwargs.items():
            set_option(setting, value)
        yield settings
    finally:
        if display_mode is not None:
            set_display_mode(orig_settings["DISPLAY_MODE"])
        for setting, value in orig_settings.items():
            # only reset it if it was adjusted originally; don't reset everything
            if setting in option_kwargs:
                set_option(setting, value)


def add_renderable_type(renderable_type: type, converter: Optional[Union[Callable, str]] = None):
    """
    Convenience function to add a type (or list of types)
    to the types that can be processed by the display formatter.
    (settings.RENDERABLE_TYPES default: [pd.Series, pd.DataFrame, np.ndarray])
    """
    settings = get_settings()
    renderable = {renderable_type: converter}
    logger.debug(f"adding `{renderable}` to {settings.RENDERABLE_TYPES=}")
    settings.RENDERABLE_TYPES.update(renderable)
