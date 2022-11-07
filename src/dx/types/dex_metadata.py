import enum
import time
import uuid
from typing import Dict, List, Optional, Union

import structlog
from pydantic import BaseModel, Field, validator
from pydantic.color import Color

from dx.types.filters import DEXFilterSettings

logger = structlog.get_logger(__name__)


# --- Enums ---
class DEXMode(enum.Enum):
    exploration = "exploration"
    presentation = "presentation"


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


class DEXColorOptions(DEXBaseModel):
    color: Optional[str]
    cond: Optional[str]
    gradient: Optional[str]
    max: Optional[float]
    min: Optional[float]
    mode: Optional[str]
    threshold_colors: Optional[str] = Field(alias="thresholdColors")
    threshold_values: Optional[List[float]] = Field(alias="thresholdValues", default_factory=list)
    scale: Optional[str]


class DEXConditionalFormatRule(DEXBaseModel):
    color_opts: DEXColorOptions = Field(alias="colorOpts")
    column_type: str = Field(alias="columnType")
    field_name: str = Field(alias="fieldName")
    id: str
    index: int
    name: str = Field(default="")


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
    annotation_rules: Optional[list] = Field(alias="annotationRules", default_factory=list)
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
    aggregation: Optional[str]
    column_position: int = Field(alias="columnPosition")
    date_format: Optional[str] = Field(alias="dateFormat")
    format: Optional[str]
    frozen: Optional[bool]
    hidden: Optional[bool]
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
    annotation_rules: Optional[list] = Field(alias="annotationRules", default_factory=list)
    chart: dict = Field(default_factory=dict)
    chart_mode: str = Field(alias="chartMode", default="grid")
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

    @validator("display_id", pre=True, always=True)
    def validate_display_id(cls, val):
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
        logger.info(f"adding {new_view=}")
        self.views.append(new_view)
