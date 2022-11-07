from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from dx.types.charts._configs import (
    DEXAreaType,
    DEXBarGroupingType,
    DEXBarLabelType,
    DEXBarProjectionTypes,
    DEXBigNumberComparison,
    DEXBoundingType,
    DEXCombinationMode,
    DEXFilteredDataOnly,
    DEXFormulaDisplay,
    DEXFunnelMode,
    DEXHierarchyType,
    DEXLayerSettings,
    DEXLineSmoothing,
    DEXLineType,
    DEXNetworkLabelContents,
    DEXNetworkType,
    DEXPieceType,
    DEXPieLabelContents,
    DEXPieLabelType,
    DEXPointType,
    DEXProBarModeType,
    DEXSortColumnsBy,
    DEXSummaryType,
    DEXSurveyDataType,
    DEXSurveyResponses,
    DEXTextDataFormat,
    DEXTrendlineType,
)
from dx.types.dex_metadata import DEXBaseModel, DEXConditionalFormatRule


class DEXChartBase(DEXBaseModel):
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
    pie_label_contents: Optional[DEXPieLabelContents] = Field(
        alias="pieLabelContents", default="name"
    )
    pie_label_type: Optional[DEXPieLabelType] = Field(alias="pieLabelType", default="rim")
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
    text_data_format: Optional[DEXTextDataFormat] = Field(
        alias="textDataFormat", default="sentence"
    )
    timeseries_sort: Optional[str] = Field(alias="timeseriesSort")
    token_metric: Optional[str] = Field(alias="tokenMetric")
    trend_line: Optional[DEXTrendlineType] = Field(alias="trendLine")
    violin_iqr: Optional[bool] = Field(alias="violinIQR")
    word_rotate: Optional[str] = Field(alias="wordRotate")
    word_color: Optional[str] = Field(alias="wordColor")
    word_data: Optional[str] = Field(alias="wordData")
    zero_baseline: Optional[bool] = Field(alias="zeroBaseline")

    class Config:
        exclude_unset = True
        fields = {"exclude": "*"}


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
