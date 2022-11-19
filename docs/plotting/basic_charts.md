# Basic Charts

Here we'll talk about how to plot some basic chart types in DEX using `dx`.

!!! example "Initial dataset"

    We will be using our own built-in DataFrame generation function for these visualizations.
    The values you see may be different if you run the same code in a cell, but the column structure should be very similar (if not identical).
    ```python
    df = dx.random_dataframe(100)
    ```
    ::: src.dx.random_dataframe

## [Bar](../../reference/basic_charts/#src.dx.plotting.dex.basic.bar)
### Basic
```python
dx.bar(df, x='keyword_column', y='integer_column')
```
![](../screenshots/plotting_bar_simple1.png)
### More options
```python

dx.bar(
    df, 
    x='keyword_column', 
    y='integer_column',
    y2='float_column',
    horizontal=True,
    bar_width='index',
    group_other=True,
    column_sort_order="desc",
    column_sort_type="string",
    pro_bar_mode="stacked",
    combination_mode="max",
    show_bar_label=True,
)
```
```
INSERT SCREENSHOT
```

## [Line](../../reference/dex_plotting/#src.dx.plotting.dex.basic.line)

### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```
## [Pie](../../reference/dex_plotting/#src.dx.plotting.dex.basic.pie)

### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```
## [Scatter](../../reference/dex_plotting/#src.dx.plotting.dex.basic.scatterplot)

### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```
## [Tilemap](../../reference/dex_plotting/#src.dx.plotting.dex.basic.tilemap)

### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```
## [Violin](../../reference/dex_plotting/#src.dx.plotting.dex.basic.violin)

### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```
## [Wordcloud](../../reference/dex_plotting/#src.dx.plotting.dex.basic.wordcloud)
### Basic
```
INSERT SCREENSHOT
```
### More options
```
INSERT SCREENSHOT
```