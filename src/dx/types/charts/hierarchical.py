from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXTreemapChartConfig(DEXChartBase):
    hierarchy_type: Literal["treemap"] = Field(alias="hierarchyType", default="treemap")

    class Config:
        fields = {
            "selected_dimensions": {"include": True},
            "metric1": {"include": True},
            "network_label": {"include": True},
            "hierarchy_type": {"include": True},
        }

class DEXSunburstChartConfig(DEXChartBase):
    hierarchy_type: Literal["sunburst"] = Field(alias="hierarchyType", default="sunburst")

    class Config:
        fields = {
            "selected_dimensions": {"include": True},
            "metric1": {"include": True},
            "network_label": {"include": True},
            "hierarchy_type": {"include": True},
        }

class DEXPartitionChartConfig(DEXChartBase):
    hierarchy_type: Literal["partition"] = Field(alias="hierarchyType", default="partition")

    class Config:
        fields = {
            "selected_dimensions": {"include": True},
            "metric1": {"include": True},
            "network_label": {"include": True},
            "hierarchy_type": {"include": True},
        }

class DEXDendrogramChartConfig(DEXChartBase):
    hierarchy_type: Literal["dendrogram"] = Field(alias="hierarchyType", default="dendrogram")

    class Config:
        fields = {
            "selected_dimensions": {"include": True},
            "network_label": {"include": True},
            "hierarchy_type": {"include": True},
        }


DEXHierarchicalChartConfig = Annotated[
    Union[
        DEXTreemapChartConfig,
        DEXSunburstChartConfig,
        DEXPartitionChartConfig,
        DEXDendrogramChartConfig,
    ],
    Field(discriminator="hierarchy_type"),
]


class DEXHierarchicalChartView(DEXView):
    chart_mode: Literal["hierarchy"] = "hierarchy"
    chart: DEXHierarchicalChartConfig


class DEXTreemapChartView(DEXHierarchicalChartView):
    chart: DEXTreemapChartConfig


class DEXSunburstChartView(DEXHierarchicalChartView):
    chart: DEXSunburstChartConfig


class DEXPartitionChartView(DEXHierarchicalChartView):
    chart: DEXPartitionChartConfig


class DEXDendrogramChartView(DEXHierarchicalChartView):
    chart: DEXDendrogramChartConfig
