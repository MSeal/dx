import enum
import uuid
from typing import Annotated, List, Literal, Optional, Union

import structlog
from pydantic import BaseModel, Field
from pydantic.color import Color

from dx.types.charts.bar import DEXBarChartView
from dx.types.charts.line import DEXLineChartView
from dx.types.charts.parcoords import DEXParcoordsChartView
from dx.types.charts.pie import DEXPieChartView
from dx.types.charts.scatter import DEXScatterChartView
from dx.types.charts.tilemap import DEXTilemapChartView
from dx.types.charts.violin import DEXViolinChartView
from dx.types.charts.wordcloud import DEXWordcloudChartView
from dx.types.dex_metadata import DEXBaseModel, DEXConditionalFormatRule
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
    hover_opts = Optional[DEXHoverOptions] = Field(default_factory=dict)
    point_size_opts: Optional[DEXPointSizeOptions] = Field(default_factory=dict)


class DEXSurveyResponses(DEXBaseModel):
    positive: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)


class DEXChartBase(BaseModel):
    """
    Model to store all possible configs used by inherited models.
    This model should not be called directly.

    Any models created from this should include their own `fields` config
    and add `{"include": True}` for any fields that should be inherited.
    """

    adjacency_list: Optional[str] = Field(alias="adjacencyList")
    area_type: Optional[DEXAreaType] = Field(alias="areaType", default="hexbin")
    bar_grouping: Optional[DEXBarGroupingType] = Field(alias="barGrouping", default="Clustered")
    bar_label: Optional[DEXBarLabelType] = Field(alias="barLabel", default="None")
    bar_projection: Optional[DEXBarProjectionTypes] = Field(alias="barProjection")
    bar_subcategory: Optional[str] = Field(alias="barSubcategory")
    base_layer: Optional[str] = Field(alias="baseLayer")
    base_layer_fill: Optional[str] = Field(alias="baseLayerFill")
    base_layer_stroke: Optional[str] = Field(alias="baseLayerStroke")
    big_number_comparison: Optional[DEXBigNumberComparison] = Field(alias="bigNumberComparison")
    big_number_second_metric: Optional[str] = Field(alias="bigNumberSecondMetric")
    bounding_settings: Optional[dict] = Field(alias="boundingSettings")
    bounding_type: Optional[DEXBoundingType] = Field(alias="boundingType")
    boxplot_outliers: Optional[bool] = Field(alias="boxplotOutliers")
    bg_color: Optional[str] = Field(alias="bgColor")
    candle_close: Optional[str] = Field(alias="candleClose")
    candle_high: Optional[str] = Field(alias="candleHigh")
    candle_low: Optional[str] = Field(alias="candleLow")
    candle_open: Optional[str] = Field(alias="candleOpen")
    candlestick_mode: Optional[bool] = Field(alias="candlestickMode")
    combination_mode: Optional[DEXCombinationMode] = Field(alias="combinationMode")
    confo_rules: Optional[List[DEXConditionalFormatRule]] = Field(
        alias="confoRules", default_factory=list
    )
    deselect_keys_hash: Optional[dict] = Field(alias="deselectKeysHash")
    dim1: Optional[str]
    dim2: Optional[str]
    dim3: Optional[str]
    edge_mode: Optional[str] = Field(alias="edgeMode")
    enforce_combined_color: Optional[bool] = Field(alias="enforceCombinedColor")
    facet_metrics: Optional[List[str]] = Field(alias="facetMetrics")
    facets: Optional[list]
    filtered_data_only: Optional[DEXFilteredDataOnly] = Field(alias="filteredDataOnly")
    formula_display: Optional[DEXFormulaDisplay] = Field(alias="formulaDisplay")
    funnel_data: Optional[str] = Field(alias="funnelData")
    funnel_metric_order: Optional[List[str]] = Field(alias="funnelMetricOrder")
    funnel_mode: Optional[DEXFunnelMode] = Field(alias="funnelMode")
    grid_size: Optional[int] = Field(alias="gridSize")
    group_other: Optional[bool] = Field(alias="groupOther")
    hierarchy_type: Optional[DEXHierarchyType] = Field(alias="hierarchyType")
    is_brushing: Optional[bool] = Field(alias="isBrushing")
    layer_settings: Optional[DEXLayerSettings] = Field(alias="layerSettings")
    line_brush: Optional[dict] = Field(alias="lineBrush")
    line_smoothing: Optional[DEXLineSmoothing] = Field(alias="lineSmoothing")
    line_type: Optional[DEXLineType] = Field(alias="lineType", default="line")
    map_mode: Optional[str] = Field(alias="mapMode")
    map_zoom: Optional[str] = Field(alias="mapZoom")
    marginal_graphics: Optional[DEXSummaryType] = Field(alias="marginalGraphics")
    metric1: Optional[str]
    metric2: Optional[str]
    metric3: Optional[str]
    metric4: Optional[str]
    multi_axis_line: Optional[bool] = Field(alias="multiAxisLine")
    network_label: Optional[str] = Field(alias="networkLabel")
    network_label_contents: Optional[DEXNetworkLabelContents] = Field(alias="networkLabelContents")
    network_type: Optional[DEXNetworkType] = Field(alias="networkType")
    override_point_size: Optional[int] = Field(alias="overridePointSize")
    par_coords_color: Optional[str] = Field(alias="parCoordsColor")
    pie_label_contents: Optional[DEXPieLabelContents] = Field(alias="pieLabelContents")
    pie_label_type: Optional[DEXPieLabelType] = Field(alias="pieLabelType")
    piece_type: Optional[DEXPieceType] = Field(alias="pieceType")
    point_bar_mode: Optional[str] = Field(alias="pointBarMode")
    point_type: Optional[DEXPointType] = Field(alias="pointType")
    primary_key: Optional[List[str]] = Field(alias="primaryKey")
    pro_bar_mode: Optional[DEXProBarModeType] = Field(alias="proBarMode")
    scatter_brush: Optional[dict] = Field(alias="scatterBrush")
    scatterplot_color: Optional[str] = Field(alias="scatterplotColor")
    scatterplot_size: Optional[str] = Field(alias="scatterplotSize")
    second_bar_metric: Optional[str] = Field(alias="secondBarMetric")
    second_metric_style: Optional[str] = Field(alias="secondMetricStyle")
    selected_dimensions: Optional[List[str]] = Field(alias="selectedDimensions")
    selected_metrics: Optional[List[Union[str, Literal["DEX_COUNT"]]]] = Field(
        alias="selectedMetrics"
    )
    selected_metrics_diverging: Optional[List[str]] = Field(alias="selectedMetricsDiverging")
    show_contours: Optional[Union[Literal["contours-only"], bool]] = Field(alias="showContours")
    show_total: Optional[bool] = Field(alias="showTotal")
    sort_columns_by: Optional[DEXSortColumnsBy] = Field(alias="sortColumnsBy")
    sparkchart: Optional[str] = Field(alias="sparkchart")
    split_lines_by: Optional[str] = Field(alias="splitLinesBy")
    splom_mode: Optional[str] = Field(alias="splomMode")
    summary_bins: Optional[int] = Field(alias="summaryBins")
    summary_type: Optional[DEXSummaryType] = Field(alias="summaryType")
    survey_data_type: Optional[DEXSurveyDataType] = Field(alias="surveyDataType")
    survey_responses: Optional[DEXSurveyResponses] = Field(alias="surveyResponses")
    text_data_format: Optional[str] = Field(alias="textDataFormat")
    timeseries_sort: Optional[str] = Field(alias="timeseriesSort")
    token_metric: Optional[str] = Field(alias="tokenMetric")
    trend_line: Optional[DEXTrendlineType] = Field(alias="trendLine")
    violin_iqr: Optional[bool] = Field(alias="violinIQR")
    word_rotate: Optional[str] = Field(alias="wordRotate")
    word_color: Optional[str] = Field(alias="wordColor")
    word_data: Optional[str] = Field(alias="wordData")
    zero_base_line: Optional[bool] = Field(alias="zeroBaseLine")

    class Config:
        exclude_unset = True
        fields = {"exclude": "*"}


DEXChartViews = Union[
    # basic
    DEXBarChartView,
    DEXLineChartView,
    DEXPieChartView,
    DEXScatterChartView,
    DEXTilemapChartView,
    DEXViolinChartView,
    DEXWordcloudChartView,
    # comparison
    DEXParcoordsChartView,
    # time series
    # relationship
    # part to whole
    # funnel
    # summary
    # map
]

DEXChartView = Annotated[DEXChartViews, Field(discriminator="chart_type")]
