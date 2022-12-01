<!-- --8<-- [start:usage] -->
## [Violin](../../reference/charts/basic_charts/#src.dx.plotting.dex.basic.violin)

### Simple
=== "dx"

    ```python
    dx.violin(df, split_by='keyword_column', metric='integer_column')
    ```
    ![](../screenshots/plotting_violin_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot(kind='violin', split_by='keyword_column', metric='integer_column')
    ```
    _*Note you can't use `df.plot.violin()` directly_

    ![](../screenshots/plotting_violin_simple1_pd.png)
    
### Customized
=== "dx"
    ```python
    dx.violin(
        df, 
        split_by='keyword_column', 
        metric='integer_column',
        bins=5,
        show_interquartile_range=True,
        column_sort_order='desc',
    )
    ```
    ![](../screenshots/plotting_violin_custom1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot(
        kind='violin',
        split_by='keyword_column', 
        metric='integer_column',
        bins=5,
        show_interquartile_range=True,
        column_sort_order='desc',
    )
    ```
    _*Note you can't use `df.plot.violin()` directly_

    ![](../screenshots/plotting_violin_custom1_pd.png)
<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:ref] -->
## [Violin](../../../plotting/basic_charts/#violin)
::: src.dx.plotting.dex.basic.violin
<!-- --8<-- [end:ref] -->