<!-- --8<-- [start:usage] -->
## [Wordcloud](../../reference/charts/basic_charts/#src.dx.plotting.dex.basic_charts.wordcloud)
### Simple
=== "dx"

    ```python
    dx.wordcloud(df, word_column='keyword_column', size='float_column')
    ```
    ![](../screenshots/plotting_wordcloud_simple1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot(kind='wordcloud', word_column='keyword_column', size='float_column')
    ```
    _*Note you can't use `df.plot.wordcloud()` directly_

    ![](../screenshots/plotting_wordcloud_simple1_pd.png)
    
### Customized
=== "dx"

    ```python
    dx.wordcloud(
        df, 
        word_column='dtype_column',
        size='float_column',
        text_format='token',
        word_rotation='45',
        random_coloring=True,
    )
    ```
    ![](../screenshots/plotting_wordcloud_custom1.png)

=== "pd.options.plotting.backend = 'dx'"

    !!! info "Make sure you [enable `dx` as a pandas plotting backend](../plotting/overview.md#enabling-pandas-plotting-backend) first."

    ```python
    df.plot(
        kind='wordcloud',
        word_column='keyword_column',
        word_column='dtype_column',
        size='float_column',
        text_format='token',
        word_rotation='45',
        random_coloring=True,
    )
    ```
    _*Note you can't use `df.plot.wordcloud()` directly_

    ![](../screenshots/plotting_wordcloud_custom1_pd.png)
<!-- --8<-- [end:usage] -->

<!-- --8<-- [start:ref] -->
## [Wordcloud](../../../plotting/basic_charts/#wordcloud)
::: src.dx.plotting.dex.basic_charts.wordcloud
<!-- --8<-- [end:ref] -->