import pytest

from dx.datatypes.main import SORTED_DX_DATATYPES, random_dataframe
from dx.utils.formatting import clean_column_values


@pytest.mark.benchmark
@pytest.mark.parametrize("dtype", SORTED_DX_DATATYPES)
def test_benchmark_column_cleaning(
    benchmark,
    dtype: str,
    num_rows: int = 50_000,
):
    params = {dt: False for dt in SORTED_DX_DATATYPES}
    params[dtype] = True
    df = random_dataframe(num_rows, **params)
    for col in df.columns:
        benchmark(clean_column_values, df[col])

    # do something else here?
    assert 1 == 1
