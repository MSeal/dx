import enum
import time
import uuid
from datetime import datetime
from typing import Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated


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


class DEXMediaType(enum.Enum):
    dataresource = "application/vnd.dataresource+json"
    dex = "application/vnd.dex.v1+json"

    def __str__(self):
        return self.value


class DEXMode(enum.Enum):
    exploration = "exploration"
    presentation = "presentation"


class DEXSampleStrategy(enum.Enum):
    first = "first"
    last = "last"
    none = "none"
    random = "random"


class DEXViewType(enum.Enum):
    public = "public"


class DEXChartMode(enum.Enum):
    grid = "grid"
    line = "line"
    summary = "summary"
    wordcloud = "wordcloud"


class DEXFieldOverrideType(enum.Enum):
    boolean = "boolean"
    datetime = "datetime"
    integer = "integer"
    number = "number"
    string = "string"


class DEXTrendlineType(enum.Enum):
    linear = "linear"
    exponential = "exponential"
    logarithmic = "logarithmic"
    power = "power"
    polynomial = "polynomial"
    none = "none"


class DEXDateFilter(BaseModel):
    column: str
    type: Literal["DATE_FILTER"] = "DATE_FILTER"
    predicate: Literal["between"] = "between"

    start: datetime
    end: datetime

    @property
    def _pd_column(self):
        return clean_pandas_column(self.column)

    @property
    def sql_filter(self) -> str:
        sql_time_fmt = "%Y-%m-%dT%H:%M:%S.%f"  # yyyy-mm-ddThh:mi:ss.mmm
        start_timestamp = pd.Timestamp(self.start).strftime(sql_time_fmt)
        end_timestamp = pd.Timestamp(self.end).strftime(sql_time_fmt)
        date_filter_min = f""""{self.column}" >= '{start_timestamp}'"""
        date_filter_max = f""""{self.column}" <= '{end_timestamp}'"""
        return f"{date_filter_min} AND {date_filter_max}"

    @property
    def pandas_filter(self) -> str:
        # any kind of .to_pydatetime() conversion will likely raise
        # InvalidComparison errors between pd.Timestamp and np.datetime64,
        # but the frontend passes UTC time, while the data may not have tzinfo
        start_timestamp = pd.Timestamp(self.start).tz_localize(None)
        end_timestamp = pd.Timestamp(self.end).tz_localize(None)
        date_filter_min = f"""({self._pd_column} >= "{start_timestamp}")"""
        date_filter_max = f"""({self._pd_column} <= "{end_timestamp}")"""
        return f"({date_filter_min} & {date_filter_max})"


class DEXDimensionFilter(BaseModel):
    column: str
    type: Literal["DIMENSION_FILTER"] = "DIMENSION_FILTER"
    predicate: Literal["in"] = "in"

    value: list

    @property
    def _pd_column(self):
        return clean_pandas_column(self.column)

    @property
    def sql_filter(self) -> str:
        quote_scaped_vals = [v.replace("'", "''").replace('"', '""') for v in self.value]
        filter_values_str = ", ".join([f"'{v}'" for v in quote_scaped_vals])
        return f""""{self.column}" IN ({filter_values_str})"""

    @property
    def pandas_filter(self) -> str:
        return f"""({self._pd_column} in {self.value})"""


class DEXMetricFilter(BaseModel):
    column: str
    type: Literal["METRIC_FILTER"] = "METRIC_FILTER"
    predicate: Literal["between"] = "between"

    value: list

    @property
    def _pd_column(self):
        return clean_pandas_column(self.column)

    @property
    def sql_filter(self) -> str:
        metric_filter_min = f""""{self.column}" >= {self.value[0]}"""
        metric_filter_max = f""""{self.column}" <= {self.value[1]}"""
        return f"{metric_filter_min} AND {metric_filter_max}"

    @property
    def pandas_filter(self) -> str:
        # `.between()` has issues here depending on the column name structure
        metric_filter_min = f"""({self._pd_column} >= {self.value[0]})"""
        metric_filter_max = f"""({self._pd_column} <= {self.value[1]})"""
        return f"({metric_filter_min} & {metric_filter_max})"


def clean_pandas_column(column: str) -> str:
    """
    Converts column names into a more pandas .query()-friendly format.
    """
    # pandas will raise errors if the columns are numeric
    # e.g. "UndefinedVariableError: name 'BACKTICK_QUOTED_STRING_{column}' is not defined"
    # so we have to refer to them as pd.Series object using `@df[column]` structure
    # except we don't know the name of the variable here, so we pass {df_name} as a placeholder
    # to be filled in by the kernel*
    # ---
    # *as of August 2022, the dx package is using this for Datalink processing and filling df_name
    # as part of its internal tracking
    if str(column).isdigit() or str(column).isdecimal():
        return f"@{{df_name}}[{column}]"
    return f"`{column}`"


FilterTypes = Union[DEXDateFilter, DEXDimensionFilter, DEXMetricFilter]


class DEXFilterSettings(BaseModel):
    SHOW_FILTER_PANEL: Optional[bool] = True
    filters: List[Annotated[FilterTypes, Field(discriminator="type")]] = []

    def to_sql_query(self) -> str:
        return " AND ".join([f.sql_filter for f in self.filters])

    def to_pandas_query(self) -> str:
        return " & ".join([f.pandas_filter for f in self.filters])


class DEXResampleMessage(BaseModel):
    display_id: str
    filters: List[Annotated[FilterTypes, Field(discriminator="type")]] = []
    limit: int = 50_000
    cell_id: Optional[str] = None


class DEXBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


# TODO: flesh this out
# class DEXConditionalFormatRule(DEXBaseModel):
#     pass


DEXConditionalFormatRule = dict


class DEXDecoration(BaseModel):
    footer: str = ""
    subtitle: str = ""
    # TODO: change this back to "Table" before merging
    title: str = "🐼 hello from dx"


class DEXDashboardViewConfig(BaseModel):
    id: str
    column: int
    row: int


class DEXDashboardView(DEXBaseModel):
    annotation_rules: Optional[dict] = Field(alias="annotationRules", default_factory=dict)
    dashboard_filter: bool = Field(alias="dashboardFilter", default=False)
    dashboard_filter_settings: dict = Field(alias="dashboardFilterSettings", default_factory=dict)
    decoration: DEXDecoration
    display_id: str = Field(alias="displayId", default_factory=uuid.uuid4)
    filter_settings: Optional[DEXFilterSettings] = Field(alias="filterSettings")
    filters: Optional[DEXFilterSettings]
    id: str  # is either 'first-view' or some UUID
    view_sizes: Optional[dict] = Field(alias="viewSizes", default_factory=dict)
    views: List[DEXDashboardViewConfig]
    views_ignoring_dashboard_filters: dict = Field(
        alias="viewsIgnoringDashboardFilters", default_factory=dict
    )


class DEXDashboard(DEXBaseModel):
    multi_views: List[DEXDashboardView] = Field(alias="multiViews")


class DEXField(DEXBaseModel):
    column_position: int = Field(alias="columnPosition")
    override_type: Optional[DEXFieldOverrideType] = Field(alias="overrideType")
    format: Optional[str]


class DEXStyleConfig(DEXBaseModel):
    colors: List[str]


class DEXView(DEXBaseModel):
    annotation_rules: Optional[dict] = Field(alias="annotationRules", default_factory=dict)
    chart: dict = Field(default_factory=dict)
    chart_mode: DEXChartMode = Field(alias="chartMode", default="grid")
    confo_rules: Optional[List[DEXConditionalFormatRule]] = Field(
        alias="confoRules", default_factory=list
    )
    decoration: Optional[DEXDecoration] = Field(default_factory=DEXDecoration)
    display_id: str = Field(alias="displayId", default_factory=uuid.uuid4)
    filter_settings: Optional[DEXFilterSettings] = Field(
        alias="filterSettings", default_factory=DEXFilterSettings
    )
    id: str = Field(default_factory=uuid.uuid4)
    is_comment: bool = Field(alias="isComment", default=False)
    is_default: bool = Field(alias="isDefault", default=False)
    is_transitory: Optional[bool] = Field(alias="isTransitory", default=False)
    type: DEXViewType = Field(default="public")
    user_id: str = Field(alias="userId", default="")
    variable_name: Optional[str] = Field(alias="variableName")

    @validator("id", pre=True, always=True)
    def validate_id(cls, val):
        return str(val)


class DEXMetadata(DEXBaseModel):
    annotations_rules_by_id: Optional[dict] = Field(alias="annotationsRulesById")
    dashboard: Optional[DEXDashboard]
    decoration: Optional[dict]
    field_metadata: Optional[Dict[str, DEXField]] = Field(
        alias="fieldMetadata", default_factory=dict
    )
    filters: Optional[dict]
    mode: Optional[DEXMode]
    simple_table: Optional[bool] = Field(alias="simpleTable", default=False)
    styles: Optional[DEXStyleConfig]
    updated: int = Field(default_factory=time.time)
    views: Optional[List[DEXView]] = Field(default_factory=list)

    @validator("updated", pre=True, always=True)
    def validate_updated(cls, val):
        val = time.time()
        return int(val)

    def add_view(self, **kwargs):
        is_default = kwargs.pop("is_default", False)
        if not self.views:
            is_default = True
        new_view = DEXView(
            is_default=is_default,
            **kwargs,
        )
        self.views.append(new_view)
