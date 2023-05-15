from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXScatterPlotMatrixConfig(DEXChartBase):
    splom_mode: Literal["none"] = Field(alias="splomMode", default="none")


class DEXCorrelationMatrixConfig(DEXChartBase):
    splom_mode: Literal["basic-matrix"] = Field(alias="splomMode", default="basic-matrix")


DEXMatrixConfigs = Annotated[
    Union[
        DEXScatterPlotMatrixConfig,
        DEXCorrelationMatrixConfig,
    ],
    Field(discriminator="splom_mode"),
]


class DEXMatrixChartView(DEXView):
    chart_mode: Literal["splom"] = "splom"
    chart: DEXMatrixConfigs


class DEXScatterPlotMatrixChartView(DEXMatrixChartView):
    chart: DEXScatterPlotMatrixConfig = Field(default_factory=DEXScatterPlotMatrixConfig)


class DEXCorrelationMatrixChartView(DEXView):
    chart: DEXCorrelationMatrixConfig = Field(default_factory=DEXCorrelationMatrixConfig)
