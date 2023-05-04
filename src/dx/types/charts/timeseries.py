from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXLineChartConfig(DEXChartBase):
    line_type: Literal["line"] = Field(alias="lineType", default="line")

    class Config:
        fields = {
            "bounding_type": {"include": True},
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "multi_axis_line": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }

class DEXCumulativeLineChartConfig(DEXChartBase):
    line_type: Literal["cumulative"] = Field(alias="lineType", default="cumulative")

    class Config:
        fields = {
            "bounding_type": {"include": True},
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }

class DEXPercentLineChartConfig(DEXChartBase):
    line_type: Literal["percentline"] = Field(alias="lineType", default="percentline")

    class Config:
        fields = {
            "bounding_type": {"include": True},
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }

class DEXStackedAreaChartConfig(DEXChartBase):
    line_type: Literal["stackedarea"] = Field(alias="lineType", default="stackedarea")

    class Config:
        fields = {
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }

class DEXPercentStackedAreaChartConfig(DEXChartBase):
    line_type: Literal["stackedpercent"] = Field(alias="lineType", default="stackedpercent")

    class Config:
        fields = {
            "combination_mode": {"include": True},
            "line_smoothing": {"include": True},
            "line_type": {"include": True},
            "selected_metrics": {"include": True},
            "split_lines_by": {"include": True},
            "timeseries_sort": {"include": True},
            "zero_baseline": {"include": True},
        }

DEXSummaryChartConfig = Annotated[
    Union[
        DEXLineChartConfig,
        DEXCumulativeLineChartConfig,
        DEXPercentLineChartConfig,
        DEXStackedAreaChartConfig,
        DEXPercentStackedAreaChartConfig,
    ],
    Field(discriminator="line_type"),
]


class DEXTimeSeriesChartView(DEXView):
    chart_mode: Literal["line"] = "line"
    chart: DEXSummaryChartConfig


class DEXLineChartView(DEXTimeSeriesChartView):
    chart: DEXLineChartConfig


class DEXCumulativeLineChartView(DEXTimeSeriesChartView):
    chart: DEXCumulativeLineChartConfig


class DEXPercentLineChartView(DEXTimeSeriesChartView):
    chart: DEXPercentLineChartConfig


class DEXStackedAreaChartView(DEXTimeSeriesChartView):
    chart: DEXStackedAreaChartConfig


class DEXPercentStackedAreaChartView(DEXTimeSeriesChartView):
    chart: DEXPercentStackedAreaChartConfig
