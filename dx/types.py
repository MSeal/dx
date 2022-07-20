import enum


class DXDisplayMode(enum.Enum):
    enhanced = "enhanced"  # GRID display
    simple = "simple"  # classic simpleTable/DEX display
    default = "default"  # basic/vanilla python/pandas display


class DXSamplingMode(enum.Enum):
    first = "first"  # df.head(num_rows)
    random = "random"  # df.sample(num_rows)
    last = "last"  # df.tail(num_rows)
