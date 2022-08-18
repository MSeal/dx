import logging
from contextlib import contextmanager
from functools import lru_cache
from typing import Optional, Set, Union

from IPython.core.interactiveshell import InteractiveShell
from pandas import set_option as pandas_set_option
from pydantic import BaseSettings, validator

from dx.types import DXDisplayMode, DXSamplingMethod

MB = 1024 * 1024


class Settings(BaseSettings):
    LOG_LEVEL = logging.DEBUG

    DISPLAY_MAX_ROWS: int = 60
    DISPLAY_MAX_COLUMNS: int = 20
    HTML_TABLE_SCHEMA: bool = False
    MEDIA_TYPE: str = "application/vnd.dataresource+json"

    MAX_RENDER_SIZE_BYTES: int = 100 * MB
    RENDERABLE_OBJECTS: Set[type] = set()

    # what percentage of the dataset to remove during each sampling
    # in order to get large datasets under MAX_RENDER_SIZE_BYTES
    SAMPLING_FACTOR: float = 0.1

    DISPLAY_MODE: DXDisplayMode = DXDisplayMode.simple

    SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.random
    COLUMN_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.random
    ROW_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.random
    # TODO: support more than just int type here
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html
    RANDOM_STATE: int = 12_648_430

    RESET_INDEX_VALUES: bool = False

    @validator("RENDERABLE_OBJECTS", pre=True, always=True)
    def validate_renderables(cls, vals):
        """Allow passing comma-separated strings or actual types."""
        if isinstance(vals, str):
            vals = vals.replace(",", "").split()
        if not isinstance(vals, set):
            vals = {vals}

        valid_vals = set()
        for val in vals:
            if isinstance(val, type):
                valid_vals.add(val)
                continue
            try:
                val_type = eval(str(val))
                valid_vals.add(val_type)
            except Exception as e:
                raise ValueError(f"can't evaluate {val} type as renderable object: {e}")

        return valid_vals

    class Config:
        validate_assignment = True


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


def set_display_mode(
    mode: DXDisplayMode = DXDisplayMode.simple,
    ipython_shell: Optional[InteractiveShell] = None,
):
    """
    Sets the display mode for the IPython formatter in the current session.
    - "plain" (vanilla python/pandas display)
    - "simple" (classic simpleTable/DEX display)
    - "enhanced" (GRID display)
    """
    # circular imports
    from dx.formatters.dataresource import deregister
    from dx.formatters.dx import register
    from dx.formatters.main import reset

    global settings
    settings.DISPLAY_MODE = mode

    if str(mode) == DXDisplayMode.enhanced.value:
        register(ipython_shell=ipython_shell)
    elif str(mode) == DXDisplayMode.simple.value:
        deregister(ipython_shell=ipython_shell)
    elif str(mode) == DXDisplayMode.plain.value:
        reset(ipython_shell=ipython_shell)
    else:
        raise ValueError(f"`{mode}` is not a supported display mode")


def set_option(
    key,
    value,
    ipython_shell: Optional[InteractiveShell] = None,
) -> None:
    key = str(key).upper()

    global settings
    if key in vars(settings):
        setattr(settings, key, value)

        # make sure pandas settings are updated as well for display sizes
        pd_options = {
            "DISPLAY_MAX_ROWS": "display.max_rows",
            "DISPLAY_MAX_COLUMNS": "display.max_columns",
            "HTML_TABLE_SCHEMA": "html.table_schema",
        }
        if key in pd_options:
            pandas_set_option(pd_options[key], value)

        # this may be the most straightforward way to handle
        # IPython display formatter changes being done through
        # settings updates for now, but I don't like it being here
        if key == "DISPLAY_MODE":
            set_display_mode(value, ipython_shell=ipython_shell)

        return
    raise ValueError(f"`{key}` is not a valid setting")


@contextmanager
def settings_context(**option_kwargs):
    global settings
    orig_settings = settings.dict()
    try:
        for setting, value in option_kwargs.items():
            set_option(setting, value)
        yield settings
    finally:
        for setting, value in orig_settings.items():
            set_option(setting, value)


def add_renderable_type(renderable_type: Union[type, list]):
    """
    Convenience function to add a type (or list of types)
    to the types that can be processed by the display formatter.
    (settings.RENDERABLE_OBJECTS default: [pd.Series, pd.DataFrame, np.ndarray])
    """
    global settings

    if not isinstance(renderable_type, list):
        renderable_type = [renderable_type]

    settings.RENDERABLE_OBJECTS.update(renderable_type)
