import enum
import uuid
from typing import List, Optional, Union

import structlog
from pydantic import Field, validator
from pydantic.color import Color

from dx.types.dex_metadata import DEXBaseModel
from dx.types.filters import DEXDimensionFilter
from dx.types.main import BaseEnum

logger = structlog.get_logger(__name__)


# --- Enums ---
class DEXAreaType(BaseEnum):
    contour = "contour"
    heatmap = "heatmap"
    hexbin = "hexbin"


class DEXBarGroupingType(BaseEnum):
    clustered = "Clustered"
    stacked = "Stacked"


class DEXBarLabelType(BaseEnum):
    none = "none"
    show = "show"


class DEXBarProjectionTypes(BaseEnum):
    horizontal = "horizontal"
    radial = "radial"
    vertical = "vertical"


class DEXBigNumberComparison(BaseEnum):
    raw = "raw"
    percent = "percent"


class DEXBoundingType(BaseEnum):
    absolute = "absolute"
    relative = "relative"


class DEXChartMode(BaseEnum):
    bar = "bar"
    bignumber = "bignumber"
    dimensionmatrix = "dimensionmatrix"
    dotplot = "dotplot"
    funnel = "funnel"
    grid = "grid"
    hexbin = "hexbin"
    hierarchy = "hierarchy"
    line = "line"
    map = "map"
    network = "network"
    parcoords = "parcoords"
    pie = "pie"
    scatter = "scatter"
    splom = "splom"
    summary = "summary"
    survey = "survey"
    tilemap = "tilemap"
    timebar = "timebar"
    wordcloud = "wordcloud"


class DEXCombinationMode(BaseEnum):
    avg = "AVG"
    count = "COUNT"
    max = "MAX"
    med = "MED"
    min = "MIN"
    sum = "SUM"


class DEXEdgeModes(BaseEnum):
    edge_list = "edge list"
    adjacency_list = "adjacency list"


class DEXFilteredDataOnly(BaseEnum):
    all_data = "All Data"
    filtered_data_only = "Filtered Data Only"


class DEXFormulaDisplay(BaseEnum):
    formula = "formula"
    none = "none"
    r2 = "r2"


class DEXFunnelMode(BaseEnum):
    bar = "bar"
    flow = "flow"
    graphic = "graphic"
    motif = "motif"
    sunburst = "sunburst"
    tree = "tree"


class DEXHierarchyType(BaseEnum):
    dendrogram = "dendrogram"
    partition = "partition"
    sunburst = "sunburst"
    treemap = "treemap"


class DEXLineSmoothing(BaseEnum):
    hourly = "hourly"
    daily = "daily"
    seven_day_moving_average = "7dma"
    weekly = "weekly"
    monthly = "monthly"
    none = "none"


class DEXLineType(BaseEnum):
    bumparea = "bumparea"
    cumulative = "cumulative"
    line = "line"
    linepercent = "linepercent"
    stackedarea = "stackedarea"
    stackedpercent = "stackedpercent"


class DEXMapLayerType(BaseEnum):
    point = "point"
    choro = "choro"


mapbox_tile_layer_conversion = {
    "streets": "streets-v11",
    "outdoors": "outdoors-v11",
    "light": "light-v10",
    "dark": "dark-v10",
    "satellite": "satellite-v9",
}


class DEXMapBoxTileLayer(BaseEnum):
    streets = "streets-v11"
    outdoors = "outdoors-v11"
    light = "light-v10"
    dark = "dark-v10"
    satellite = "satellite-v9"


class DEXNetworkLabelContents(BaseEnum):
    id = "id"
    value = "value"
    id_value = "id-value"


class DEXNetworkType(BaseEnum):
    arc = "arc"
    force = "force"
    matrix = "matrix"
    sankey = "sankey"


class DEXPieLabelContents(BaseEnum):
    name = "name"
    value = "value"
    percent = "percent"
    name_value = "name-value"
    name_percent = "name-percent"
    value_percent = "value-percent"


class DEXPieLabelType(BaseEnum):
    annotation = "annotation"
    stem = "stem"
    center = "center"
    none = "none"
    rim = "rim"


class DEXPieceType(BaseEnum):
    bar = "bar"
    clusterbar = "clusterbar"
    point = "point"
    swarm = "swarm"


class DEXPointType(BaseEnum):
    bar = "Bar"
    dotplot = "Dot Plot"
    lollipop = "Lollipop"


class DEXPointSizeMode(BaseEnum):
    fixed = "fixed"
    functional = "functional"


class DEXProBarModeType(BaseEnum):
    clustered = "Clustered"
    combined = "Combined"
    stacked = "Stacked"


class DEXScale(BaseEnum):
    linear = "Linear"
    log = "Log"


class DEXSecondMetricstyle(BaseEnum):
    bar = "bar"
    dot = "dot"


class DEXSortColumnsByOrder(enum.Enum):
    asc = "asc"
    desc = "desc"


class DEXSortColumnsByType(enum.Enum):
    int = "int"
    date = "date"
    string = "string"


class DEXSortColumnsBy(BaseEnum):
    asc_col_string = "asc-col-string"
    asc_col_int = "asc-col-int"
    asc_col_date = "asc-col-date"
    desc_col_string = "desc-col-string"
    desc_col_int = "desc-col-int"
    desc_col_date = "desc-col-date"


class DEXSplomMode(BaseEnum):
    contour = "contour"
    correlation = "correlation"


class DEXSummaryType(BaseEnum):
    boxplot = "boxplot"
    heatmap = "heatmap"
    histogram = "histogram"
    horizon = "horizon"
    joy = "joy"
    none = "none"
    ridgeline = "ridgeline"
    violin = "violin"


class DEXSurveyDataType(BaseEnum):
    row = "row"
    column = "column"


class DEXTrendlineType(BaseEnum):
    exponential = "exponential"
    linear = "linear"
    logarithmic = "logarithmic"
    none = "none"
    polynomial = "polynomial"
    power = "power"


class DEXTextDataFormat(BaseEnum):
    sentence = "sentence"
    token = "token"


class DEXWordRotate(BaseEnum):
    r45 = 45
    r90 = 90
    jitter = "jitter"
    none = "none"


# --- Models ---
class DEXChartFacetFilter(DEXBaseModel):
    filter: DEXDimensionFilter


class DEXChartFacet(DEXBaseModel):
    title: str
    name: str
    filtering: DEXChartFacetFilter


class DEXHoverOptions(DEXBaseModel):
    dims: Optional[List[str]] = Field(default_factory=list)
    mets: Optional[List[str]] = Field(default_factory=list)


class DEXPointSizeOptions(DEXBaseModel):
    mode: Optional[DEXPointSizeMode]
    size: Optional[int]
    met: Optional[str]
    scale: Optional[DEXScale]
    min: Optional[int]
    max: Optional[int]
    size_min: Optional[int] = Field(alias="sizeMin", gte=0, lte=10)
    size_max: Optional[int] = Field(alias="sizeMax", gte=0, lte=10)

    @validator("scale", pre=True, always=True)
    def validate_scale(cls, v):
        return str(v).title()


class DEXLayerSettings(DEXBaseModel):
    size: Optional[Union[str, int]] = 2
    stroke: Optional[Union[str, Color]] = "#000000"
    stroke_width: Optional[int] = Field(alias="strokeWidth", default=2, gte=0, lte=10)
    transparency: Optional[float] = Field(gte=0.1, lte=1.0)
    type: Optional[DEXMapLayerType] = "point"
    lat_dim: str = Field(alias="latDim")
    long_dim: str = Field(alias="longDim")
    id: str = Field(default_factory=uuid.uuid4)
    hover_opts: Optional[DEXHoverOptions] = Field(alias="hoverOpts")
    point_size_opts: Optional[DEXPointSizeOptions] = Field(alias="pointSizeOpts")
    show_labels: Optional[str] = Field(alias="showLabels")
    tile_layer: Optional[DEXMapBoxTileLayer] = Field(
        alias="tileLayer", default=DEXMapBoxTileLayer.streets
    )

    @validator("stroke", pre=True, always=True)
    def validate_color(cls, v):
        """"""
        if isinstance(v, Color):
            return v.as_hex()
        try:
            # make sure we can turn the string into a color and return it as-is; this is because passing a shortened hex value like
            # "#00f" will not be recognized, but "#0000ff" will.
            Color(v)
            return v
        except Exception as e:
            logger.exception(f"failed to recognize {v} as a color: {e}")

    @validator("tile_layer", pre=True, always=True)
    def validate_tile_layer(cls, v):
        return mapbox_tile_layer_conversion[v]

    @validator("id", pre=True, always=True)
    def validate_id(cls, val):
        return str(val)


class DEXSurveyResponses(DEXBaseModel):
    positive: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)
