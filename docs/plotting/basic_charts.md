# Basic Charts

Here we'll talk about how to plot some basic chart types in DEX using `dx`.

<!-- --8<-- [start:setup] -->
## Setup
We will be using our own built-in DataFrame generation function for these visualizations.
The values you see may be different if you run the same code in a cell, but the column structure should be very similar (if not identical).
```python
df = dx.random_dataframe(100)
```

!!! warning "The _**Customized**_ examples with more options do not necessarily represent "good" data visualization; they are just a glimpse into what settings are available to compare against the _**Simple**_ examples."    
<!-- --8<-- [end:setup] -->

--8<-- "bar.md:usage"
--8<-- "line.md:usage"
--8<-- "pie.md:usage"
--8<-- "scatter.md:usage"
--8<-- "tilemap.md:usage"
--8<-- "violin.md:usage"
--8<-- "wordcloud.md:usage"
