# Basic Charts

Here we'll talk about how to plot some basic chart types in DEX using `dx`.

<!-- --8<-- [start:intro] -->
We will be using our own built-in DataFrame generation function for these visualizations.
The values you see may be different if you run the same code in a cell, but the column structure should be very similar (if not identical).
```python
df = dx.random_dataframe(100)
```

!!! warning "The _**Customized**_ examples with more options do not necessarily represent "good" data visualization; they are just a glimpse into what settings are available to compare with the simple examples."    
<!-- --8<-- [end:intro] -->

--8<-- "./docs/_charts/bar.md:usage"

--8<-- "./docs/_charts/line.md:usage"

--8<-- "./docs/_charts/pie.md:usage"

--8<-- "./docs/_charts/scatter.md:usage"

--8<-- "./docs/_charts/tilemap.md:usage"

--8<-- "./docs/_charts/violin.md:usage"

--8<-- "./docs/_charts/wordcloud.md:usage"
