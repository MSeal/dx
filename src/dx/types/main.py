import enum

import structlog

logger = structlog.get_logger(__name__)


# --- Enums ---
class BaseEnum(enum.Enum):
    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(other) == self.value


class DXDisplayMode(BaseEnum):
    enhanced = "enhanced"  # GRID display
    simple = "simple"  # classic simpleTable/DEX display
    plain = "plain"  # basic/vanilla python/pandas display


class DXSamplingMethod(BaseEnum):
    first = "first"  # df.head(num_rows)
    inner = "inner"  # middle rows
    last = "last"  # df.tail(num_rows)
    outer = "outer"  # df.head(num_rows/2) & df.tail(num_rows/2)
    random = "random"  # df.sample(num_rows)


class DEXMediaType(BaseEnum):
    dataresource = "application/vnd.dataresource+json"
    dex = "application/vnd.dex.v1+json"
