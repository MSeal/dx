from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDotPlotConfig(DEXChartBase):
    bar_projection: Literal["horizontal"] = Field(alias="barProjection", default="horizontal")
    column_line: bool = Field(alias="columnLine", default=False)


class DEXRadarPlotConfig(DEXChartBase):
    bar_projection: Literal["radial"] = Field(alias="barProjection", default="radial")
    column_line: bool = Field(alias="columnLine", default=False)


class DEXColumnLineConfig(DEXRadarPlotConfig):
    column_line: bool = Field(alias="columnLine", default=True)


DEXRadialPlotConfig = Annotated[
    Union[
        DEXRadarPlotConfig,
        DEXColumnLineConfig,
    ],
    Field(discriminator="column_line"),
]


DEXGenericDotPlotConfigs = Annotated[
    Union[
        DEXDotPlotConfig,
        DEXRadialPlotConfig,
    ],
    Field(discriminator="bar_projection"),
]


class DEXGenericDotPlotChartView(DEXView):
    chart_mode: Literal["dotplot"] = "dotplot"
    chart: DEXGenericDotPlotConfigs


class DEXDotPlotChartView(DEXGenericDotPlotChartView):
    chart: DEXDotPlotConfig = Field(default_factory=DEXDotPlotConfig)


class DEXRadarPlotChartView(DEXGenericDotPlotChartView):
    chart: DEXRadarPlotConfig = Field(default_factory=DEXRadarPlotConfig)


class DEXColumnLineChartView(DEXGenericDotPlotChartView):
    chart: DEXColumnLineConfig = Field(default_factory=DEXColumnLineConfig)
