# dx

<p align="center">
This package provides convenient formatting and IPython display formatter registration for tabular data and DEX media types.
</p>
<p align="center">
<a href="https://github.com/noteable-io/dx/actions/workflows/ci.yaml">
    <img src="https://github.com/noteable-io/dx/actions/workflows/ci.yaml/badge.svg" alt="CI" />
</a>
<a href="https://codecov.io/gh/noteable-io/dx" > 
 <img src="https://codecov.io/gh/noteable-io/dx/branch/main/graph/badge.svg?token=RGNWOIPWC0" alt="codecov code coverage"/> 
 </a>
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/dx" />
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dx" />
<img alt="PyPI" src="https://img.shields.io/pypi/v/dx">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

---------

A Pythonic Data Explorer, open sourced with ❤️ by <a href="https://noteable.io">Noteable</a>, a collaborative notebook platform that enables teams to use and visualize data, together.


## Requirements

Python 3.8+

## Installation

### Poetry

```shell
poetry add dx
```

Then import the package:

```python
import dx
```

### Pip
```shell
pip install dx
```

Then import the package:

```python
import dx
```

## Usage

The `dx` library currently enables DEX media type visualization of pandas `DataFrame` and `Series` objects, as well as numpy `ndarray` objects. This can be handled in two ways:
- individual calls to `dx.display()`
- updating the current IPython display formatter for a session

### With `dx.display()`
`dx.display()` will display a single dataset using the DEX media type. It currently supports:
- pandas `DataFrame` objects
  ```python
  import pandas as pd
  import random

  df = pd.DataFrame({
      'random_ints': [random.randint(0, 100) for _ in range(500)],
      'random_floats': [random.random() for _ in range(500)],
  })
  dx.display(df)
  ```
  <mark>REPLACE SCREENSHOT HERE</mark>

- tabular data as `dict` or `list` types
  ```python
  dx.display([
    [1, 5, 10, 20, 500],
    [1, 2, 3, 4, 5],
    [0, 0, 0, 0, 1]
  ])
  ```
  <mark>REPLACE SCREENSHOT HERE</mark>

- `.csv` or `.json` filepaths 

  <mark>REPLACE SCREENSHOT HERE</mark>

### With `dx.register()` and `dx.deregister()`
`dx` will update the current `IPython` display formatters to allow DEX media type visualization of pandas `DataFrame` objects for an entire notebook / kernel session instead of the default `DataFrame` display output.
> Note: this **only** affects pandas DataFrames; it does not affect the display of `.csv`/`.json` file data, or `dict`/`list` outputs

- `dx.register()`
  
  ```python
  import pandas as pd

  # enable DEX display outputs from now on
  dx.register()

  df = pd.read_csv("examples/sample_data.csv")
  df
  ```
  ```python
  df2 = pd.DataFrame(
      [
          [1, 5, 10, 20, 500],
          [1, 2, 3, np.nan, 5],
          [0, 0, 0, np.nan, 1]
      ],
      columns=['a', 'b', 'c', 'd', 'e']
  )
  df2
  ```
  <mark>REPLACE SCREENSHOT HERE</mark>

- `dx.deregister()`
  
  ```python
  df2 = pd.DataFrame(
      [
          [1, 5, 10, 20, 500],
          [1, 2, 3, np.nan, 5],
          [0, 0, 0, np.nan, 1]
      ],
      columns=['a', 'b', 'c', 'd', 'e']
  )
  df2
  ```
  ```python
  dx.deregister()
  df2
  ```
  <mark>REPLACE SCREENSHOT HERE</mark>


### Settings
<mark>FILL THIS OUT</mark>


### Examples

For more examples see the [`examples`](./examples).

## Contributing

See [CONTRIBUTING.md](https://github.com/noteable-io/dx/blob/main/CONTRIBUTING.md).

## Code of Conduct

We follow the noteable.io [code of conduct](CODE_OF_CONDUCT.md).

## LICENSE

See [LICENSE.md](LICENSE.md).

-------

<p align="center">Open sourced with ❤️ by <a href="https://noteable.io">Noteable</a> for the community.</p>

<img href="https://pages.noteable.io/private-beta-access" src="https://assets.noteable.io/github/2022-07-29/noteable.png" alt="Boost Data Collaboration with Notebooks">