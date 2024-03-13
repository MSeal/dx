<!-- --8<-- [start:usage] -->
## [Scatter](../../reference/charts/basic_charts/#src.dx.plotting.dex.basic_charts.scatterplot)

### Simple
=== "dx"

    ```python
    dx.scatter(df, x='float_column', y='integer_column')
    ```
    ![](../screenshots/plotting_scatter_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    !!! bug "Known Issue"
        `df.plot.scatter()` can be used unless `size` is specified. If you wish to use pandas syntax and provide a `size` argument, please use `df.plot(kind='scatter', ...)`.

    ```python
    df.plot(kind='scatter', x='float_column', y='integer_column')
    ```
    ![](../screenshots/plotting_scatter_simple1_pd.png)
    
### Customized
=== "dx"

    ```python
    dx.scatter(
        df, 
        x='float_column', 
        y='integer_column',
        size='index',
        trend_line='polynomial',
        marginal_graphics='histogram',
        formula_display='r2'
    )
    ```
    ![](../screenshots/plotting_scatter_custom1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    !!! bug "Known Issue"
        `df.plot.scatter()` can be used unless `size` is specified. If you wish to use pandas syntax and provide a `size` argument, please use `df.plot(kind='scatter', ...)`.

    ```python
    df.plot(
        kind='scatter',
        x='float_column', 
        y='integer_column',
        size='index',
        trend_line='polynomial',
        marginal_graphics='histogram',
        formula_display='r2'
    )
    ```
    ![](../screenshots/plotting_scatter_custom1_pd.png)
<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:ref] -->
## [Scatter](../../../plotting/basic_charts/#scatter)
::: src.dx.plotting.dex.basic_charts.scatter
<!-- --8<-- [end:ref] -->