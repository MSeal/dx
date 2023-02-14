import enum
import time
import uuid
from datetime import datetime
from typing import Dict, List, Literal, Optional, Union

import structlog
from pydantic import BaseModel, Field, validator
from pydantic.color import Color
from typing_extensions import Annotated

from dx.types.filters import DEXFilterSettings

logger = structlog.get_logger(__name__)


# --- Enums ---


class DEXColorMode(enum.Enum):
    fixed = "fixed"
    gradient = "gradient"
    threshold = "threshold"
    functional = "functional"


class DEXFunctionalCondition(enum.Enum):
    contains = "contains"
    # TODO: flesh this out


class DEXGradient(enum.Enum):
    turbo = "turbo"

    # TODO: flesh this out
    def __str__(self):
        return str(self.value).title()


color_schemes = {
    "blues": "blues5",
    "reds": "reds5",
    "purple_orange": "PuOr5",
    "red_yellow_green": "RdYlGn5",
    # TODO: flesh this out
}


class DEXColorScheme(enum.Enum):
    blues = "blues5"
    reds = "reds5"
    purple_orange = "purple_orange"
    red_yellow_green = "red_yellow_green"

    def __str__(self):
        return color_schemes(self.value)


class DEXMode(enum.Enum):
    exploration = "exploration"
    presentation = "presentation"


class DEXConfoScale(enum.Enum):
    linear = "linear"
    log = "log"

    def __str__(self):
        return str(self.value).title()


class DEXViewType(enum.Enum):
    public = "public"


class DEXFieldOverrideType(enum.Enum):
    boolean = "boolean"
    datetime = "datetime"
    integer = "integer"
    number = "number"
    string = "string"


# --- Models ---
class DEXBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        extra = "allow"


class DEXColorOptions(DEXBaseModel):
    color: Optional[str]
    cond: Optional[str]
    gradient: Optional[str]
    max: Optional[float]
    min: Optional[float]
    mode: DEXColorMode = DEXColorMode.fixed
    threshold_colors: Optional[str] = Field(alias="thresholdColors")
    threshold_values: List[float] = Field(alias="thresholdValues", default_factory=list)
    scale: Optional[str]


class DEXFixedColorOptions(DEXColorOptions):
    mode: Literal["fixed"] = "fixed"
    color: Color
    min: Union[float, int]
    max: Union[float, int]


class DEXFunctionalColorOptions(DEXColorOptions):
    mode: Literal["functional"] = "functional"
    color: Color
    cond: DEXFunctionalCondition
    min: Union[bool, int, float, str, datetime]
    max: Union[bool, int, float, str, datetime]


class DEXGradientColorOptions(DEXColorOptions):
    mode: Literal["gradient"] = "gradient"
    gradient: DEXGradient
    min: Union[float, int]
    max: Union[float, int]
    scale: DEXConfoScale = DEXConfoScale.linear


class DEXThresholdColorOptions(DEXColorOptions):
    mode: Literal["threshold"] = "threshold"
    min: Union[float, int]
    max: Union[float, int]
    threshold_colors: DEXColorScheme = DEXColorScheme.red_yellow_green
    threshold_values: List[float] = Field(default_factory=list)


ColorOpts = Union[
    DEXFixedColorOptions,
    DEXFunctionalColorOptions,
    DEXGradientColorOptions,
    DEXThresholdColorOptions,
]


class DEXConditionalFormatRule(DEXBaseModel):
    color_opts: List[Annotated[ColorOpts, Field(discriminator="mode")]] = Field(
        alias="colorOpts", default_factory=list
    )
    column_type: str = Field(alias="columnType")
    field_name: str = Field(alias="fieldName")
    id: str = Field(default_factory=uuid.uuid4)
    index: int
    name: str = Field(default="")


class DEXDecoration(BaseModel):
    footer: str = ""
    subtitle: str = ""
    title: str = "Table"


class DEXDashboardViewConfig(BaseModel):
    id: str
    column: int
    row: int


class DEXField(DEXBaseModel):
    aggregation: Optional[str]
    column_position: int = Field(alias="columnPosition")
    date_format: Optional[str] = Field(alias="dateFormat")
    format: Optional[str]
    frozen: bool
    hidden: bool
    name: Optional[str]
    override_type: Optional[DEXFieldOverrideType] = Field(alias="overrideType")
    sort: Optional[str]
    width: Optional[str]


class DEXStyleConfig(DEXBaseModel):
    colors: List[Union[str, Color]]

    @validator("colors", pre=True, always=True)
    def validate_color(cls, v):
        colors = []
        for color in v:
            if not isinstance(color, Color):
                color = Color(color)
            colors.append(color.as_hex())
        return colors


class DEXView(DEXBaseModel):
    annotation_rules: list = Field(alias="annotationRules", default_factory=list)
    chart: dict = Field(default_factory=dict)
    chart_mode: str = Field(alias="chartMode", default="grid")
    confo_rules: List[DEXConditionalFormatRule] = Field(alias="confoRules", default_factory=list)
    dashboard_filter: bool = Field(alias="dashboardFilter", default=False)
    dashboard_filter_settings: dict = Field(alias="dashboardFilterSettings", default_factory=dict)
    decoration: DEXDecoration = Field(default_factory=DEXDecoration)
    display_id: str = Field(alias="displayId", default_factory=uuid.uuid4)
    filter_settings: DEXFilterSettings = Field(
        alias="filterSettings", default_factory=DEXFilterSettings
    )
    filters: DEXFilterSettings = Field(default_factory=DEXFilterSettings)
    id: str = Field(default_factory=uuid.uuid4)
    is_comment: bool = Field(alias="isComment", default=False)
    is_default: bool = Field(alias="isDefault", default=False)
    is_transitory: bool = Field(alias="isTransitory", default=False)
    programmatic: bool = Field(default=True)
    type: DEXViewType = Field(default="public")
    user_id: str = Field(alias="userId", default="dx")
    variable_name: Optional[str] = Field(alias="variableName")
    view_sizes: dict = Field(alias="viewSizes", default_factory=dict)
    views_ignoring_dashboard_filters: dict = Field(
        alias="viewsIgnoringDashboardFilters", default_factory=dict
    )

    @validator("id", pre=True, always=True)
    def validate_id(cls, val):
        return str(val)

    @validator("display_id", pre=True, always=True)
    def validate_display_id(cls, val):
        return str(val)


class DEXDashboard(DEXBaseModel):
    multi_views: List[DEXView] = Field(alias="multiViews")


class DEXMetadata(DEXBaseModel):
    annotations_rules_by_id: Optional[dict] = Field(alias="annotationsRulesById")
    dashboard: Optional[DEXDashboard]
    decoration: Optional[dict]
    field_metadata: Dict[str, DEXField] = Field(alias="fieldMetadata", default_factory=dict)
    filters: dict = Field(default_factory=dict)
    mode: DEXMode = DEXMode.exploration
    simple_table: bool = Field(alias="simpleTable", default=False)
    styles: Optional[DEXStyleConfig]
    updated: int = Field(default_factory=time.time)
    views: List[DEXView] = Field(default_factory=list)

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
        logger.debug(f"adding {new_view=}")
        self.views.append(new_view)
