# dx

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nteract/dx/main?urlpath=nteract/tree/examples)

A Pythonic Data Explorer.

## Install

For Python 3.8+:

```
pip install dx
```

## Usage

The `dx` library contains a simple helper function also called `dx`.

```python
from dx import dx
```

`dx()` takes one positional argument, a `dataframe`.

```python
dx.display(dataframe)
```

The `dx(dataframe)` function will display the dataframe in
[data explorer](https://github.com/nteract/data-explorer) mode:

In the future, other data sources may be supported.

### Example

```python
import dx
import pandas as pd

# Get happiness data and create a pandas dataframe
df = pd.read_csv('examples/sample_data.csv')

# Open data explorer with the happiness dataframe
dx.display(df)
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