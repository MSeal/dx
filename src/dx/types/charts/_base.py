from typing import List, Literal, Optional, Union

from pydantic import Field, validator
from typing_extensions import Annotated

from dx.types.charts import options
from dx.types.dex_metadata import DEXBaseModel, DEXConditionalFormatRule

TITLECASE_OPTIONS = [
    "bar_grouping",
    "filtered_data_only",
    "point_type",
    "pro_bar_mode",
]
UPPERCASE_OPTIONS = ["combination_mode"]


class DEXChartBase(DEXBaseModel):
    """
    Model to store all possible configs used by inherited models.
    This model should not be called directly.

    Any models created from this should include their own `fields` options
    and add `{"include": True}` for any fields that should be inherited.
    """

    adjacency_list: Optional[str] = Field(alias="adjacencyList")
    area_type: options.DEXAreaType = Field(alias="areaType", default="hexbin")
    bar_grouping: options.DEXBarGroupingType = Field(alias="barGrouping", default="Clustered")
    bar_label: options.DEXBarLabelType = Field(alias="barLabel", default="none")
    bar_projection: Optional[options.DEXBarProjectionTypes] = Field(alias="barProjection")
    bar_subcategory: Optional[str] = Field(alias="barSubcategory")
    base_layer: Optional[str] = Field(alias="baseLayer")
    base_layer_fill: Optional[str] = Field(alias="baseLayerFill")
    base_layer_stroke: Optional[str] = Field(alias="baseLayerStroke")
    big_number_comparison: Optional[options.DEXBigNumberComparison] = Field(
        alias="bigNumberComparison"
    )
    big_number_second_metric: Optional[str] = Field(alias="bigNumberSecondMetric")
    bounding_settings: Optional[dict] = Field(alias="boundingSettings")
    bounding_type: Optional[options.DEXBoundingType] = Field(alias="boundingType")
    boxplot_outliers: Optional[bool] = Field(alias="boxplotOutliers")
    bg_color: Optional[str] = Field(alias="bgColor")
    candle_close: Optional[str] = Field(alias="candleClose")
    candle_high: Optional[str] = Field(alias="candleHigh")
    candle_low: Optional[str] = Field(alias="candleLow")
    candle_open: Optional[str] = Field(alias="candleOpen")
    candlestick_mode: Optional[bool] = Field(alias="candlestickMode")
    combination_mode: Optional[options.DEXCombinationMode] = Field(alias="combinationMode")
    confo_rules: List[DEXConditionalFormatRule] = Field(alias="confoRules", default_factory=list)
    csp_order: Optional[str] = Field(alias="cspOrder")
    deselect_keys_hash: Optional[dict] = Field(alias="deselectKeysHash")
    dim1: Optional[str]
    dim2: Optional[str]
    dim3: Optional[str]
    edge_mode: Optional[str] = Field(alias="edgeMode")
    enforce_combined_color: Optional[bool] = Field(alias="enforceCombinedColor")
    facet_metrics: Optional[List[str]] = Field(alias="facetMetrics")
    facets: Optional[list]
    filtered_data_only: Optional[options.DEXFilteredDataOnly] = Field(alias="filteredDataOnly")
    formula_display: Optional[options.DEXFormulaDisplay] = Field(alias="formulaDisplay")
    funnel_data: Optional[str] = Field(alias="funnelData")
    funnel_metric_order: Optional[List[str]] = Field(alias="funnelMetricOrder")
    funnel_mode: Optional[options.DEXFunnelMode] = Field(alias="funnelMode")
    grid_size: Optional[int] = Field(alias="gridSize")
    group_other: Optional[bool] = Field(alias="groupOther")
    hierarchy_type: Optional[options.DEXHierarchyType] = Field(alias="hierarchyType")
    is_brushing: Optional[bool] = Field(alias="isBrushing")
    layer_settings: Optional[List[options.DEXLayerSettings]] = Field(alias="layerSettings")
    line_brush: Optional[dict] = Field(alias="lineBrush")
    line_smoothing: Optional[options.DEXLineSmoothing] = Field(alias="lineSmoothing")
    line_type: options.DEXLineType = Field(alias="lineType", default="line")
    map_mode: Optional[str] = Field(alias="mapMode")
    map_zoom: Optional[str] = Field(alias="mapZoom")
    marginal_graphics: Optional[options.DEXSummaryType] = Field(alias="marginalGraphics")
    metric1: Optional[str]
    metric2: Optional[str]
    metric3: Optional[str]
    metric4: Optional[str]
    multi_axis_line: Optional[bool] = Field(alias="multiAxisLine")
    network_label: Optional[str] = Field(alias="networkLabel")
    network_label_contents: Optional[options.DEXNetworkLabelContents] = Field(
        alias="networkLabelContents"
    )
    network_type: Optional[options.DEXNetworkType] = Field(alias="networkType")
    override_point_size: Optional[int] = Field(alias="overridePointSize")
    par_coords_color: Optional[str] = Field(alias="parCoordsColor")
    pie_label_contents: options.DEXPieLabelContents = Field(
        alias="pieLabelContents", default="name"
    )
    pie_label_type: options.DEXPieLabelType = Field(alias="pieLabelType", default="rim")
    piece_type: Optional[options.DEXPieceType] = Field(alias="pieceType")
    point_bar_mode: Optional[str] = Field(alias="pointBarMode")
    point_type: Optional[options.DEXPointType] = Field(alias="pointType")
    primary_key: Optional[List[str]] = Field(alias="primaryKey")
    pro_bar_mode: Optional[options.DEXProBarModeType] = Field(alias="proBarMode")
    scatter_brush: Optional[dict] = Field(alias="scatterBrush")
    scatterplot_color: Optional[str] = Field(alias="scatterplotColor")
    scatterplot_size: Optional[str] = Field(alias="scatterplotSize")
    second_bar_metric: Optional[str] = Field(alias="secondBarMetric")
    second_metric_style: options.DEXSecondMetricstyle = Field(
        alias="secondMetricStyle", default="bar"
    )
    selected_dimensions: Optional[List[str]] = Field(alias="selectedDimensions")
    selected_metrics: Optional[List[Union[str, Literal["DEX_COUNT"]]]] = Field(
        alias="selectedMetrics"
    )
    selected_metrics_diverging: Optional[List[str]] = Field(alias="selectedMetricsDiverging")
    show_contours: Optional[Union[Literal["contours-only"], bool]] = Field(alias="showContours")
    show_total: Optional[bool] = Field(alias="showTotal")
    sort_columns_by: Optional[options.DEXSortColumnsBy] = Field(alias="sortColumnsBy")
    sparkchart: Optional[str] = Field(alias="sparkchart")
    split_lines_by: Optional[str] = Field(alias="splitLinesBy")
    splom_mode: Optional[str] = Field(alias="splomMode")
    summary_bins: Optional[int] = Field(alias="summaryBins")
    summary_type: Optional[options.DEXSummaryType] = Field(alias="summaryType")
    survey_data_type: Optional[options.DEXSurveyDataType] = Field(alias="surveyDataType")
    survey_responses: Optional[options.DEXSurveyResponses] = Field(alias="surveyResponses")
    text_data_format: Optional[options.DEXTextDataFormat] = Field(
        alias="textDataFormat", default="sentence"
    )
    timeseries_sort: Optional[str] = Field(alias="timeseriesSort")
    token_metric: Optional[str] = Field(alias="tokenMetric")
    trend_line: Optional[options.DEXTrendlineType] = Field(alias="trendLine")
    violin_iqr: Optional[bool] = Field(alias="violinIQR")
    word_rotate: Optional[str] = Field(alias="wordRotate")
    word_color: Optional[str] = Field(alias="wordColor")
    word_data: Optional[str] = Field(alias="wordData")
    zero_baseline: Optional[bool] = Field(alias="zeroBaseline")

    @validator(*TITLECASE_OPTIONS, pre=True, always=True)
    def validate_title_case(cls, v):
        if v is None:
            return v
        return str(v).title()

    @validator(*UPPERCASE_OPTIONS, pre=True, always=True)
    def validate_upper_case(cls, v):
        if v is None:
            return v
        return str(v).upper()


def chart_view_ref():
    # avoiding circular import and ForwardRef issues
    from dx.types.charts.bar import DEXBarChartView
    from dx.types.charts.line import DEXLineChartView
    from dx.types.charts.parcoords import DEXParcoordsChartView
    from dx.types.charts.pie import DEXPieChartView
    from dx.types.charts.scatter import DEXScatterChartView
    from dx.types.charts.tilemap import DEXTilemapChartView
    from dx.types.charts.violin import DEXViolinChartView
    from dx.types.charts.wordcloud import DEXWordcloudChartView

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

    return Annotated[DEXChartViews, Field(discriminator="chart_mode")]
