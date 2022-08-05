import numpy as np
import pandas as pd


def random_dataframe(
    num_rows: int = 5,
    num_cols: int = 2,
    dtype: str = "float",
    factor: float = 1.0,
) -> pd.DataFrame:
    data = np.random.rand(num_rows, num_cols) * factor
    df = pd.DataFrame(data)
    return df.astype(dtype, errors="ignore")
