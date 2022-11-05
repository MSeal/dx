import enum
from typing import List, Literal, Optional, Union

import structlog
from pydantic import BaseModel, Field, validator

from dx.types.dex_metadata import DEXBaseModel, DEXConditionalFormatRule, DEXView
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


class DEXBarProjectionTypes(enum.Enum):
    horizontal = "horizontal"
    radial = "radial"
    vertical = "vertical"


class DEXBigNumberComparison(enum.Enum):
    raw = "raw"
    percent = "percent"


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


class DEXCombinationTypes(enum.Enum):
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


class DEXProBarModeType(enum.Enum):
    clustered = "Clustered"
    combined = "Combined"
    stacked = "Stacked"


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


class DEXSurveyResponses(DEXBaseModel):
    positive: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)


class DEXChartConfig(BaseModel):
    adjacency_list: Optional[str] = Field(alias="adjacencyList")
    area_type: Optional[DEXAreaType] = Field(alias="areaType", default="hexbin")
    bar_grouping: Optional[DEXBarGroupingType] = Field(alias="barGrouping", default="Clustered")
    bar_projection: Optional[DEXBarProjectionTypes] = Field(alias="barProjection")
    bar_subcategory: Optional[str] = Field(alias="barSubcategory")
    base_layer: Optional[str] = Field(alias="baseLayer")
    base_layer_fill: Optional[str] = Field(alias="baseLayerFill")
    base_layer_stroke: Optional[str] = Field(alias="baseLayerStroke")
    bounding_settings: Optional[dict] = Field(alias="boundingSettings")
    bounding_type: Optional[str] = Field(alias="boundingType")
    bg_color: Optional[str] = Field(alias="bgColor")
    candle_close: Optional[str] = Field(alias="candleClose")
    candle_high: Optional[str] = Field(alias="candleHigh")
    candle_low: Optional[str] = Field(alias="candleLow")
    candle_open: Optional[str] = Field(alias="candleOpen")
    candlestick_mode: Optional[bool] = Field(alias="candlestickMode")
    combination_mode: Optional[DEXCombinationTypes] = Field(alias="combinationMode")
    confo_rules: Optional[List[DEXConditionalFormatRule]] = Field(
        alias="confoRules", default_factory=list
    )
    deselect_keys_hash: Optional[dict] = Field(alias="deselectKeysHash")
    dim1: Optional[str]
    dim2: Optional[str]
    dim3: Optional[str]
    edge_mode: Optional[str] = Field(alias="edgeMode")
    facet_metrics: Optional[List[str]] = Field(alias="facetMetrics")
    filtered_data_only: Optional[DEXFilteredDataOnly] = Field(alias="filteredDataOnly")
    formula_display: Optional[DEXFormulaDisplay] = Field(alias="formulaDisplay")
    funnel_data: Optional[str] = Field(alias="funnelData")
    funnel_metric_order: Optional[List[str]] = Field(alias="funnelMetricOrder")
    funnel_mode: Optional[DEXFunnelMode] = Field(alias="funnelMode")
    hierarchy_type: Optional[DEXHierarchyType] = Field(alias="hierarchyType")
    layer_settings: Optional[str] = Field(alias="layerSettings")
    line_smoothing: Optional[str] = Field(alias="lineSmoothing")
    line_type: Optional[DEXLineType] = Field(alias="lineType", default="line")
    map_mode: Optional[str] = Field(alias="mapMode")
    map_zoom: Optional[str] = Field(alias="mapZoom")
    marginal_graphics: Optional[DEXSummaryType] = Field(alias="marginalGraphics")
    metric1: Optional[str]
    metric2: Optional[str]
    metric3: Optional[str]
    metric4: Optional[str]
    network_label: Optional[str] = Field(alias="networkLabel")
    network_type: Optional[DEXNetworkType] = Field(alias="networkType")
    override_point_size: Optional[int] = Field(alias="overridePointSize")
    par_coords_color: Optional[str] = Field(alias="parCoordsColor")
    piece_type: Optional[DEXPieceType] = Field(alias="pieceType")
    point_bar_mode: Optional[str] = Field(alias="pointBarMode")
    primary_key: Optional[List[str]] = Field(alias="primaryKey")
    pro_bar_mode: Optional[DEXProBarModeType] = Field(alias="proBarMode")
    scatterplot_color: Optional[str] = Field(alias="scatterplotColor")
    scatterplot_size: Optional[str] = Field(alias="scatterplotSize")
    second_bar_metric: Optional[str] = Field(alias="secondBarMetric")
    selected_dimensions: Optional[List[str]] = Field(alias="selectedDimensions")
    selected_metrics: Optional[List[str]] = Field(alias="selectedMetrics")
    show_contours: Optional[Union[Literal["contours-only"], bool]] = Field(alias="showContours")
    show_total: Optional[bool] = Field(alias="showTotal")
    sort_columns_by: Optional[str] = Field(alias="sortColumnsBy")
    sparkchart: Optional[str] = Field(alias="sparkchart")
    split_lines_by: Optional[str] = Field(alias="splitLinesBy")
    splom_mode: Optional[str] = Field(alias="splomMode")
    summary_bins: Optional[int] = Field(alias="summaryBins")
    summary_type: Optional[DEXSummaryType] = Field(alias="summaryType")
    survey_responses: Optional[DEXSurveyResponses] = Field(alias="surveyResponses")
    timeseries_sort: Optional[str] = Field(alias="timeseriesSort")
    trend_line: Optional[DEXTrendlineType] = Field(alias="trendLine")

    # --------

    point_type: Optional[DEXPointType] = Field(alias="pointType")
    group_other: Optional[bool] = Field(alias="groupOther")
    enforce_combined_color: Optional[bool] = Field(alias="enforceCombinedColor")
    violin_iqr: Optional[bool] = Field(alias="violinIQR")
    boxplot_outliers: Optional[bool] = Field(alias="boxplotOutliers")
    word_rotate: Optional[str] = Field(alias="wordRotate")
    word_color: Optional[str] = Field(alias="wordColor")
    word_data: Optional[str] = Field(alias="wordData")
    text_data_format: Optional[str] = Field(alias="textDataFormat")
    token_metric: Optional[str] = Field(alias="tokenMetric")
    second_metric_style: Optional[str] = Field(alias="secondMetricStyle")
    grid_size: Optional[int] = Field(alias="gridSize")
    multi_axis_line: Optional[bool] = Field(alias="multiAxisLine")
    zero_base_line: Optional[bool] = Field(alias="zeroBaseLine")
    survey_data_type: Optional[DEXSurveyDataType] = Field(alias="surveyDataType")
    selected_metrics_diverging: Optional[List[str]] = Field(alias="selectedMetricsDiverging")
    facets: Optional[list]
    is_brushing: Optional[bool] = Field(alias="isBrushing")
    line_brush: Optional[dict] = Field(alias="lineBrush")
    scatter_brush: Optional[dict] = Field(alias="scatterBrush")
    pie_label_type: Optional[DEXPieLabelType] = Field(alias="pieLabelType")
    pie_label_contents: Optional[DEXPieLabelContents] = Field(alias="pieLabelContents")
    network_label_contents: Optional[DEXNetworkLabelContents] = Field(alias="networkLabelContents")
    big_number_second_metric: Optional[str] = Field(alias="bigNumberSecondMetric")
    big_number_comparison: Optional[DEXBigNumberComparison] = Field(alias="bigNumberComparison")

    class Config:
        exclude_unset = True


class DEXChartBaseModel(DEXBaseModel):
    class Config:
        exclude = {
            "chart_type",
        }


class DEXParcoordsChart(DEXChartBaseModel):
    chart_type: Literal["parcoords"] = "parcoords"
    filtered_data_only: Optional[DEXFilteredDataOnly] = Field(alias="filteredDataOnly")
    par_coords_color: Optional[str] = Field(alias="parCoordsColor")


class DEXScatterChart(DEXChartBaseModel):
    chart_type: Literal["scatter"] = "scatter"
    formula_display: Optional[DEXFormulaDisplay] = Field(alias="formulaDisplay")
    metric1: str
    metric2: str
    scatterplot_size: Optional[str] = Field(alias="scatterplotSize")
    selected_metrics: Optional[List[str]] = Field(alias="selectedMetrics", default_factory=list)
    show_contours: Optional[Union[Literal["contours-only"], bool]] = Field(alias="showContours")
    splom_mode: Optional[DEXSplomMode] = Field(alias="splomMode")
    trend_line: Optional[DEXTrendlineType] = Field(alias="trendLine")


class DEXChartView(DEXView):
    chart_mode: DEXChartMode
    chart: DEXChartConfig

    @validator("chart", pre=True, always=True)
    def validate_chart(cls, val, values):
        chart_mode = values.get("chart_mode")
        if chart_mode is None:
            raise ValueError("chart_mode must be set")

        if chart_mode == "parcoords":
            return DEXParcoordsChart.parse_obj(val)
        elif chart_mode == "scatter":
            return DEXScatterChart.parse_obj(val)

        raise NotImplementedError(f"{chart_mode=} not implemented yet")
