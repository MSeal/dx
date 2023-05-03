<!-- --8<-- [start:usage] -->
## [Bar](../../reference/charts/basic_charts/#src.dx.plotting.dex.basic_charts.bar)
### Simple
=== "dx"

    ```python
    dx.bar(df, x='keyword_column', y='integer_column')
    ```
    ![](../screenshots/plotting_bar_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

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

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

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
<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:ref] -->
## [Bar](../../../plotting/basic_charts/#bar)
::: src.dx.plotting.dex.basic_charts.bar
<!-- --8<-- [end:ref] -->