# Overview

If you've ever worked with DEX, you may come up with the perfect visualization or dashboard and want to carry it with you to other notebooks. This can be accomplished by using `dx`'s built-in convenience functions.

## Using pandas DataFrame `.attrs`
Set `.attrs` to customize your DEX display any time your pandas DataFrame is displayed.
```python
df.attrs = {
    'noteable': {
        'decoration': {
            'title': "my super cool DEX dataframe"
        }
    }
}
df
```

## Plotting

### Supported Charts

- #### [Basic Charts](../plotting/basic_charts.md)
    * [x] [Bar](../plotting/basic_charts.md#bar)
    * [x] [Line](../plotting/basic_charts.md#line)
    * [x] [Pie](../plotting/basic_charts.md#pie)
    * [x] [Scatterplot](../plotting/basic_charts.md#scatterplot)
    * [x] [Violin](../plotting/basic_charts.md#violin)
    * [x] [Wordcloud](../plotting/basic_charts.md#wordcloud)

- #### [Comparison Charts](../plotting/comparison_charts.md)
    * [ ] Parallel Coordinates
    * [x] [Scatterplot](../plotting/basic_charts.md#scatterplot)
    * [x] [Connected Scatterplot](../plotting/basic_charts.md#scatterplot)
    * [ ] Scatterplot Matrix
    * [ ] Correlation Matrix
    * [ ] [Bar](#)
    * [ ] Dot Plot
    * [ ] Radar Plot
    * [ ] Diverging Bar
  
- #### [Time Series Charts](../plotting/time_series_charts.md)
    * [x] [Line](../plotting/basic_charts.md#line)
    * [ ] Cumulative
    * [ ] Stacked Area
    * [ ] Line Percent
    * [ ] Stacked Percent
    * [ ] Candlestick

- #### [Relationship Charts](../plotting/relationship_charts.md)
    * [ ] Force-directed Network
    * [ ] Sankey
    * [ ] Arc Diagram
    * [ ] Adjacency Matrix
    * [ ] Dendrogram

- #### [Part-to-whole Charts](../plotting/part_to_whole_charts.md)
    * [x] [Pie](../plotting/basic_charts.md#pie)
    * [ ] Donut
    * [ ] Sunburst
    * [ ] Treemap
    * [ ] Partition

- #### [Funnel Charts](../plotting/funnel_charts.md)
    * [ ] Funnel
    * [ ] Funnel Chart
    * [ ] Funnel Tree
    * [ ] Funnel Sunburst
    * [ ] Flow Diagram
    * [ ] Arc Flow

- #### [Summary Charts](../plotting/summary_charts.md)
    * [ ] Big Number
    * [x] [Wordcloud](../plotting/basic_charts.md#wordcloud)
    * [ ] Dimension Matrix
    * [x] [Violin](../plotting/basic_charts.md#violin)
    * [ ] Box Plot
    * [ ] Heat Map
    * [ ] Histogram
    * [ ] Ridgeline
    * [ ] Horizon
    * [ ] Hexbin

- #### [Maps](../plotting/maps.md)
    * [ ] Choropleth
    * [x] [Tilemap](../plotting/basic_charts.md#tilemap)

### Enabling pandas plotting backend
To enable the `dx` plotting backend and use `DataFrame.plot._____` syntax, you can run either of the following:
```python
dx.enable_plotting_backend()
```
Or
```python
pd.options.plotting.backend = "dx"
```
(They currently do the same thing, but `dx.enable_plotting_backend()` may handle more convenience functionality in the future.)