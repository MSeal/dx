from functools import lru_cache

from pydantic import BaseSettings, Field

from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER, DXDisplayFormatter
from dx.settings import get_settings
from dx.shell import get_ipython_shell

settings = get_settings()


class DXSettings(BaseSettings):
    DX_DISPLAY_MAX_ROWS: int = 50_000
    DX_DISPLAY_MAX_COLUMNS: int = 50
    DX_MAX_STRING_LENGTH: int = 250
    DX_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DX_MEDIA_TYPE: str = Field("application/vnd.dex.v1+json", allow_mutation=False)

    DX_FLATTEN_INDEX_VALUES: bool = False
    DX_FLATTEN_COLUMN_VALUES: bool = True
    DX_STRINGIFY_INDEX_VALUES: bool = False
    DX_STRINGIFY_COLUMN_VALUES: bool = True

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_dx_settings():
    return DXSettings()


dx_settings = get_dx_settings()


def register() -> None:
    """
    Enables the DEX media type output display formatting and
    updates global dx & pandas settings with DX settings.
    """
    settings.DISPLAY_MODE = "enhanced"

    settings_to_apply = {
        "DISPLAY_MAX_COLUMNS",
        "DISPLAY_MAX_ROWS",
        "MAX_STRING_LENGTH",
        "MEDIA_TYPE",
        "FLATTEN_INDEX_VALUES",
        "FLATTEN_COLUMN_VALUES",
        "STRINGIFY_INDEX_VALUES",
        "STRINGIFY_COLUMN_VALUES",
    }
    for setting in settings_to_apply:
        val = getattr(dx_settings, f"DX_{setting}", None)
        setattr(settings, setting, val)

    custom_formatter = DXDisplayFormatter()
    custom_formatter.formatters = DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters
    get_ipython_shell().display_formatter = custom_formatter
