import enum

DATARESOURCE_MEDIA_TYPE = "application/vnd.dataresource+json"
DX_MEDIA_TYPE = "application/vnd.dex.v1+json"


class DXDisplayMode(enum.Enum):
    enhanced = "enhanced"  # GRID display
    simple = "simple"  # classic simpleTable/DEX display
    default = "default"  # basic/vanilla python/pandas display
