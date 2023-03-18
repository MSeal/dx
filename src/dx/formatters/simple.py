from functools import lru_cache

from pydantic import BaseSettings, Field

from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER, DXDisplayFormatter
from dx.settings import get_settings
from dx.shell import get_ipython_shell

settings = get_settings()


class DataResourceSettings(BaseSettings):
    # "simple" (classic simpleTable/DEX) display mode
    DATARESOURCE_DISPLAY_MAX_ROWS: int = 50_000
    DATARESOURCE_DISPLAY_MAX_COLUMNS: int = 50
    DATARESOURCE_MAX_STRING_LENGTH: int = 250
    DATARESOURCE_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DATARESOURCE_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", allow_mutation=False)

    DATARESOURCE_FLATTEN_INDEX_VALUES: bool = False
    DATARESOURCE_FLATTEN_COLUMN_VALUES: bool = True
    DATARESOURCE_STRINGIFY_INDEX_VALUES: bool = False
    DATARESOURCE_STRINGIFY_COLUMN_VALUES: bool = True

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_dataresource_settings():
    return DataResourceSettings()


dataresource_settings = get_dataresource_settings()


def deregister() -> None:
    """
    Sets the current IPython display formatter as the dataresource
    display formatter, used for simpleTable / "classic DEX" outputs
    and updates global dx & pandas settings with dataresource settings.
    """
    settings.DISPLAY_MODE = "simple"

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
        val = getattr(dataresource_settings, f"DATARESOURCE_{setting}", None)
        setattr(settings, setting, val)

    custom_formatter = DXDisplayFormatter()
    custom_formatter.formatters = DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters
    get_ipython_shell().display_formatter = custom_formatter
