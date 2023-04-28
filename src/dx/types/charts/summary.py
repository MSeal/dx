from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXBoxplotChartConfig(DEXChartBase):
    summary_type: Literal["boxplot"] = Field(alias="summaryType", default="boxplot")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "boxplot_outliers": {"include": True},
        }


class DEXHeatmapChartConfig(DEXChartBase):
    summary_type: Literal["heatmap"] = Field(alias="summaryType", default="heatmap")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXHistogramChartConfig(DEXChartBase):
    summary_type: Literal["histogram"] = Field(alias="summaryType", default="histogram")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXHorizonChartConfig(DEXChartBase):
    summary_type: Literal["horizon"] = Field(alias="summaryType", default="horizon")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXRidgelineChartConfig(DEXChartBase):
    summary_type: Literal["ridgeline"] = Field(alias="summaryType", default="ridgeline")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
        }


class DEXViolinChartConfig(DEXChartBase):
    summary_type: Literal["violin"] = Field(alias="summaryType", default="violin")

    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "sort_columns_by": {"include": True},
            "summary_type": {"include": True},
            "summary_bins": {"include": True},
            "violin_iqr": {"include": True},
        }


DEXSummaryChartConfig = Annotated[
    Union[
        DEXBoxplotChartConfig,
        DEXHeatmapChartConfig,
        DEXHistogramChartConfig,
        DEXHorizonChartConfig,
        DEXRidgelineChartConfig,
        DEXViolinChartConfig,
    ],
    Field(discriminator="summary_type"),
]


class DEXSummaryChartView(DEXView):
    chart_mode: Literal["summary"] = "summary"
    chart: DEXSummaryChartConfig


class DEXBoxplotChartView(DEXSummaryChartView):
    chart: DEXBoxplotChartConfig


class DEXHeatmapChartView(DEXSummaryChartView):
    chart: DEXHeatmapChartConfig


class DEXHistogramChartView(DEXSummaryChartView):
    chart: DEXHistogramChartConfig


class DEXHorizonChartView(DEXSummaryChartView):
    chart: DEXHorizonChartConfig


class DEXRidgelineChartView(DEXSummaryChartView):
    chart: DEXRidgelineChartConfig


class DEXViolinChartView(DEXSummaryChartView):
    chart: DEXViolinChartConfig
