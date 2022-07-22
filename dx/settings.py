from functools import lru_cache

from pydantic import BaseSettings

from dx.types import DXDisplayMode, DXSamplingMethod

MB = 1024 * 1024


class Settings(BaseSettings):
    # "enhanced" (GRID) display mode
    DISPLAY_MAX_ROWS: int = 60
    DISPLAY_MAX_COLUMNS: int = 20
    HTML_TABLE_SCHEMA: bool = False
    MEDIA_TYPE: str = "application/vnd.dataresource+json"

    MAX_RENDER_SIZE_BYTES: int = 1 * MB

    # what percentage of the dataset to remove during each truncation
    # in order to get large datasets under MAX_RENDER_SIZE_BYTES
    TRUNCATION_FACTOR: float = 0.1

    DISPLAY_MODE: DXDisplayMode = DXDisplayMode.simple

    SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.outer
    COLUMN_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.outer
    ROW_SAMPLING_METHOD: DXSamplingMethod = DXSamplingMethod.outer
    # TODO: support more than just int type here
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html
    RANDOM_STATE: int = 12_648_430


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


def set_display_mode(mode: DXDisplayMode = DXDisplayMode.simple):
    """
    Sets the display mode for the IPython formatter in the current session.
    - "default" (vanilla python/pandas display)
    - "simple" (classic simpleTable/DEX display)
    - "enhanced" (GRID display)
    """
    # circular imports
    from dx.formatters.dataresource import deregister
    from dx.formatters.dx import register
    from dx.formatters.main import reset

    global settings
    settings.DISPLAY_MODE = mode

    if mode == "enhanced":
        register()
    elif mode == "simple":
        deregister()
    elif mode == "default":
        reset()


def set_option(key, value) -> None:
    global settings
    if getattr(settings, key, None):
        setattr(settings, key, value)

        # this may be the most straightforward way to handle
        # IPython display formatter changes being done through
        # settings updates for now, but I don't like it being here
        if key == "DISPLAY_MODE":
            set_display_mode(value)

        return
    raise ValueError(f"{key} is not a valid setting")
