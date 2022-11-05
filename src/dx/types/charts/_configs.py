import enum
import uuid
from typing import List, Optional

import structlog
from pydantic import BaseModel, Field
from pydantic.color import Color

from dx.types.dex_metadata import DEXBaseModel
from dx.types.filters import DEXDimensionFilter

logger = structlog.get_logger(__name__)


# --- Enums ---
class DEXAreaType(enum.Enum):
    contour = "contour"
    heatmap = "heatmap"
    hexbin = "hexbin"


class DEXBarGroupingType(enum.Enum):
    clustered = "Clustered"
    stacked = "Stacked"


class DEXBarLabelType(enum.Enum):
    none = "none"
    show = "show"


class DEXBarProjectionTypes(enum.Enum):
    horizontal = "horizontal"
    radial = "radial"
    vertical = "vertical"


class DEXBigNumberComparison(enum.Enum):
    raw = "raw"
    percent = "percent"


class DEXBoundingType(enum.Enum):
    absolute = "absolute"
    relative = "relative"


class DEXChartMode(enum.Enum):
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


class DEXCombinationMode(enum.Enum):
    avg = "AVG"
    count = "COUNT"
    max = "MAX"
    med = "MED"
    min = "MIN"
    sum = "SUM"


class DEXEdgeModes(enum.Enum):
    edge_list = "edge list"
    adjacency_list = "adjacency list"


class DEXFilteredDataOnly(enum.Enum):
    all_data = "All Data"
    filtered_data_only = "Filtered Data Only"


class DEXFormulaDisplay(enum.Enum):
    formula = "formula"
    none = "none"
    r2 = "r2"


class DEXFunnelMode(enum.Enum):
    bar = "bar"
    flow = "flow"
    graphic = "graphic"
    motif = "motif"
    sunburst = "sunburst"
    tree = "tree"


class DEXHierarchyType(enum.Enum):
    dendrogram = "dendrogram"
    partition = "partition"
    sunburst = "sunburst"
    treemap = "treemap"


class DEXLineSmoothing(enum.Enum):
    hourly = "hourly"
    daily = "daily"
    seven_day_moving_average = "7dma"
    weekly = "weekly"
    monthly = "monthly"
    none = "none"


class DEXLineType(enum.Enum):
    bumparea = "bumparea"
    cumulative = "cumulative"
    line = "line"
    linepercent = "linepercent"
    stackedarea = "stackedarea"
    stackedpercent = "stackedpercent"


class DEXNetworkLabelContents(enum.Enum):
    id = "id"
    value = "value"
    id_value = "id-value"


class DEXNetworkType(enum.Enum):
    arc = "arc"
    force = "force"
    matrix = "matrix"
    sankey = "sankey"


class DEXPieLabelContents(enum.Enum):
    name = "name"
    value = "value"
    percent = "percent"
    name_value = "name-value"
    name_percent = "name-percent"
    value_percent = "value-percent"


class DEXPieLabelType(enum.Enum):
    annotation = "annotation"
    stem = "stem"
    center = "center"
    none = "none"
    rim = "rim"


class DEXPieceType(enum.Enum):
    bar = "bar"
    clusterbar = "clusterbar"
    point = "point"
    swarm = "swarm"


class DEXPointType(enum.Enum):
    bar = "Bar"
    dotplot = "Dot Plot"
    lollipop = "Lollipop"


class DEXPointSizeMode(enum.Enum):
    fixed = "fixed"
    functional = "functional"


class DEXProBarModeType(enum.Enum):
    clustered = "Clustered"
    combined = "Combined"
    stacked = "Stacked"


class DEXScale(enum.Enum):
    linear = "linear"
    log = "log"


class DEXSortColumnsBy(enum.Enum):
    asc_col_string = "asc-col-string"
    asc_col_int = "asc-col-int"
    asc_col_date = "asc-col-date"
    desc_col_string = "desc-col-string"
    desc_col_int = "desc-col-int"
    desc_col_date = "desc-col-date"


class DEXSplomMode(enum.Enum):
    contour = "contour"
    correlation = "correlation"


class DEXSummaryType(enum.Enum):
    boxplot = "boxplot"
    heatmap = "heatmap"
    histogram = "histogram"
    horizon = "horizon"
    joy = "joy"
    none = "none"
    ridgeline = "ridgeline"
    violin = "violin"


class DEXSurveyDataType(enum.Enum):
    row = "row"
    column = "column"


class DEXTrendlineType(enum.Enum):
    exponential = "exponential"
    linear = "linear"
    logarithmic = "logarithmic"
    none = "none"
    polynomial = "polynomial"
    power = "power"


# --- Models ---
class DEXChartFacetFilter(DEXBaseModel):
    filter: DEXDimensionFilter


class DEXChartFacet(DEXBaseModel):
    title: str
    name: str
    filtering: DEXChartFacetFilter


class DEXHoverOptions(BaseModel):
    dims: Optional[List[str]] = Field(default_factory=list)
    mets: Optional[List[str]] = Field(default_factory=list)


class DEXPointSizeOptions(BaseModel):
    mode: Optional[DEXPointSizeMode]
    size: Optional[int]
    met: Optional[str]
    scale: Optional[DEXScale]
    min: Optional[int]
    max: Optional[int]
    size_min: Optional[int] = Field(alias="sizeMin", gte=0, lte=10)
    size_max: Optional[int] = Field(alias="sizeMax", gte=0, lte=10)


class DEXLayerSettings(BaseModel):
    color: Optional[Color] = "#000000"
    size: Optional[int] = 2
    stroke: Optional[Color] = "#000000"
    stroke_width: Optional[int] = Field(alias="strokeWidth", default=2, gte=0, lte=10)
    transparency: Optional[float] = Field(gte=0.1, lte=1.0)
    type: Optional[str] = "point"
    lat_dim: str = Field(alias="latDim")
    long_dim: str = Field(alias="longDim")
    id: str = Field(default_factory=uuid.uuid4)
    hover_opts: Optional[DEXHoverOptions] = Field(default_factory=DEXHoverOptions)
    point_size_opts: Optional[DEXPointSizeOptions] = Field(default_factory=dict)


class DEXSurveyResponses(DEXBaseModel):
    positive: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)
