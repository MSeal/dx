# dx

A Pythonic Data Explorer.

## Install

For Python 3.8+:
```
pip install dx>=1.0.0
```

## Usage

The `dx` library allows for enabling/disabling DEX media type visualization with `dx.enable()` and `dx.display(data)` by setting a custom `IPython` formatter.

```python
import dx

dx.enable()
```

### Example

```python
import pandas as pd

# load randomized number/bool/string data
df = pd.read_csv('examples/sample_data.csv')
dx.display(df)
```

Pass `index=True` to visualize the `.index` values of a dataframe as well as the column/row values:
```python
dx.display(df, index=True)
```

If you only wish to display a certain number of rows from the dataframe, use
a context and specify the max rows (if set to None, all rows are used):

```python
# To use the first 13 rows for visualization with dx
with pd.option_context('display.max_rows', 13):
  dx.display(df)
```

## Develop

```
git clone https://github.com/noteable-io/dx
cd ./dx
pip install -e .
```



## Code of Conduct

We follow the noteable.io code of conduct.

## LICENSE

See [LICENSE.md](LICENSE.md).