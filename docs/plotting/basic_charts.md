# Basic Charts

Here we'll talk about how to plot some basic chart types in DEX using `dx`.

We will be using our own built-in DataFrame generation function for these visualizations.
The values you see may be different if you run the same code in a cell, but the column structure should be very similar (if not identical).
```python
df = dx.random_dataframe(100)
```

!!! warning "The _**Customized**_ examples with more options do not necessarily represent "good" data visualization; they are just a glimpse into what settings are available to compare with the simple examples."    

## [Bar](../../reference/basic_charts/#src.dx.plotting.dex.basic.bar)
### Simple
=== "dx"

    ```python
    dx.bar(df, x='keyword_column', y='integer_column')
    ```
    ![](../screenshots/plotting_bar_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot.bar(x='keyword_column', y='integer_column')
    ```
    ![](../screenshots/plotting_bar_simple1_pd.png)

### Customized

=== "dx"

    ```python
    dx.bar(
        df, 
        x='keyword_column', 
        y='integer_column',
        y2='float_column',
        y2_style='dot',
        horizontal=True,
        bar_width='index',
        group_other=True,
        column_sort_order="desc",
        column_sort_type="string",
        pro_bar_mode="combined",
        combination_mode="max",
        show_bar_labels=True,
    )
    ```
    ![](../screenshots/plotting_bar_custom1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot.bar(
        x='keyword_column', 
        y='integer_column',
        y2='float_column',
        y2_style='dot',
        horizontal=True,
        bar_width='index',
        group_other=True,
        column_sort_order="desc",
        column_sort_type="string",
        pro_bar_mode="combined",
        combination_mode="max",
        show_bar_labels=True,
    )
    ```
    ![](../screenshots/plotting_bar_custom1_pd.png)

## [Line](../../reference/dex_plotting/#src.dx.plotting.dex.basic.line)

### Simple
=== "dx"

    ```python
    dx.line(df, x='datetime_column', y='integer_column')
    ```
    ![](../screenshots/plotting_line_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot.line(x='datetime_column', y='integer_column')
    ```
    ![](../screenshots/plotting_line_simple1_pd.png)
    
### Customized
You may need to use a larger dataset to see the changes here. For these examples, we used `dx.random_dataframe(5000)`.

=== "dx"
    ```python
    dx.line(
        df, 
        x='datetime_column', 
        y='integer_column',
        line_type="cumulative",
        split_by="keyword_column",
        multi_axis=True,
        smoothing="hourly",
        use_count=True,
        bounding_type="relative",
        zero_baseline=True,
        combination_mode="min",
    )
    ```
    ![](../screenshots/plotting_line_custom1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](overview.md#enabling-pandas-plotting-backend) first."

    ```python
    dx.line(
        df, 
        x='datetime_column', 
        y='integer_column',
        line_type="cumulative",
        split_by="keyword_column",
        multi_axis=True,
        smoothing="hourly",
        use_count=True,
        bounding_type="relative",
        zero_baseline=True,
        combination_mode="min",
    )
    ```
    ![](../screenshots/plotting_line_custom1_pd.png)

    
## [Pie](../../reference/dex_plotting/#src.dx.plotting.dex.basic.pie)

### Simple
```
INSERT SCREENSHOT
```
### Customized
```
INSERT SCREENSHOT
```
## [Scatter](../../reference/dex_plotting/#src.dx.plotting.dex.basic.scatterplot)

### Simple
```
INSERT SCREENSHOT
```
### Customized
```
INSERT SCREENSHOT
```
## [Tilemap](../../reference/dex_plotting/#src.dx.plotting.dex.basic.tilemap)

### Simple
```
INSERT SCREENSHOT
```
### Customized
```
INSERT SCREENSHOT
```
## [Violin](../../reference/dex_plotting/#src.dx.plotting.dex.basic.violin)

### Simple
```
INSERT SCREENSHOT
```
### Customized
```
INSERT SCREENSHOT
```
## [Wordcloud](../../reference/dex_plotting/#src.dx.plotting.dex.basic.wordcloud)
### Simple
```
INSERT SCREENSHOT
```
### Customized
```
INSERT SCREENSHOT
```