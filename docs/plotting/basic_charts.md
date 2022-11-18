# Basic Charts

Here we'll talk about how to plot some basic chart in DEX types using `dx`.

## [Bar](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.bar)
### Basic
```python
df = dx.random_dataframe(100)
dx.bar(df, x='keyword_column', y='integer_column')
```
### More options
```python
df = dx.random_dataframe(100)
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
)
```
<iframe src="https://app.noteable.io/f/677f51aa-cc42-4066-b7fe-ce1d9b0cef51/dx-demo-notebook.ipynb?cellID=6374edfb-0a75-4e59-b5bd-eb9d8c290f6e"/>

## [Line](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.line)

```
INSERT SCREENSHOT
```
## [Pie](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.pie)

```
INSERT SCREENSHOT
```
## [Scatterplot](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.scatterplot)

```
INSERT SCREENSHOT
```
## [Tilemap](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.tilemap)

```
INSERT SCREENSHOT
```
## [Violin](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.violin)

```
INSERT SCREENSHOT
```
## [Wordcloud](https://noteable-io.github.io/dx/reference/dex_plotting/#src.dx.plotting.dex.basic.wordcloud)
```
INSERT SCREENSHOT
```