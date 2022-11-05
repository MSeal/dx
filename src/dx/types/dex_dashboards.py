import uuid
from typing import List, Optional

import structlog
from pydantic import BaseModel, Field

from dx.types.dex_metadata import DEXBaseModel, DEXDecoration
from dx.types.filters import DEXFilterSettings

logger = structlog.get_logger(__name__)


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
