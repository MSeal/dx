from functools import lru_cache

from pydantic import BaseSettings, Field

from dx.types import DXDisplayMode, DXSamplingMode

MB = 1024 * 1024


class Settings(BaseSettings):
    # "enhanced" (GRID) display mode
    DX_DISPLAY_MAX_ROWS: int = 100_000
    DX_DISPLAY_MAX_COLUMNS: int = 50
    DX_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DX_MEDIA_TYPE: str = Field("application/vnd.dex.v1+json", allow_mutation=False)

    # "simple" (classic simpleTable/DEX) display mode
    DATARESOURCE_DISPLAY_MAX_ROWS: int = 100_000
    DATARESOURCE_DISPLAY_MAX_COLUMNS: int = 50
    DATARESOURCE_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DATARESOURCE_MEDIA_TYPE: str = Field(
        "application/vnd.dataresource+json", allow_mutation=False
    )

    # "default" (pandas) display mode
    PANDAS_DISPLAY_MAX_ROWS: int = 60
    PANDAS_DISPLAY_MAX_COLUMNS: int = 20
    PANDAS_HTML_TABLE_SCHEMA: bool = Field(False, allow_mutation=False)

    MAX_RENDER_SIZE_BYTES: int = 1 * MB

    # what percentage of the dataset to remove during each truncation
    # in order to get large datasets under MAX_RENDER_SIZE_BYTES
    TRUNCATION_FACTOR: float = 0.1

    DISPLAY_MODE: DXDisplayMode = DXDisplayMode.simple
    SAMPLING_MODE: DXSamplingMode = DXSamplingMode.random

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`


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


def set_max_render_size_bytes(size: int) -> None:
    """
    Set the maximum size of dataframes that will be sent to the frontend.
    """
    global settings
    settings.MAX_RENDER_SIZE_BYTES = size


def set_sampling_mode(mode: DXSamplingMode = DXSamplingMode.random):
    """
    Sets the sampling mode for the IPython formatter in the current session.
    - "random" (random sampling)
    - "first" (first row)
    - "last" (last row)
    """
    global settings
    settings.SAMPLING_MODE = mode


def set_truncation_factor(factor: float = 0.05):
    """
    Sets the truncation factor for reducing large dataframes before rendering.
    (Does not affect original dataset; only the truncated version is sent
    to the frontend.)
    """
    global settings
    settings.TRUNCATION_FACTOR = factor
