import enum


class DXDisplayMode(enum.Enum):
    enhanced = "enhanced"  # GRID display
    simple = "simple"  # classic simpleTable/DEX display
    plain = "plain"  # basic/vanilla python/pandas display

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(other) == self.value


class DXSamplingMethod(enum.Enum):
    first = "first"  # df.head(num_rows)
    outer = "outer"  # df.head(num_rows/2) & df.tail(num_rows/2)
    inner = "inner"  # middle rows
    random = "random"  # df.sample(num_rows)
    last = "last"  # df.tail(num_rows)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(other) == self.value
