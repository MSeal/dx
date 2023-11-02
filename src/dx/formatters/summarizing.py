from typing import Callable

import pandas as pd


class DataFrameSummarizer:
    _instance: "DataFrameSummarizer" = None
    summarizing_func: Callable | None = None

    def __init__(self, summarizing_func: Callable | None = None):
        self.summarizing_func = summarizing_func

        self._load_repr_llm()

    def _load_repr_llm(self) -> None:
        """Load repr_llm's summarize_dataframe into the summarizing_func if it's available."""
        try:
            from repr_llm.pandas import summarize_dataframe

            self.summarizing_func = summarize_dataframe
        except ImportError:
            return

    @classmethod
    def instance(cls) -> "DataFrameSummarizer":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def summarize(self, df: pd.DataFrame) -> str:
        """Generate a summary of a dataframe using the configured summarizing_func."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("`df` must be a pandas DataFrame")

        if self.summarizing_func is None:
            return df.describe().to_string()

        return self.summarizing_func(df)


def get_summarizing_function() -> Callable | None:
    """Get the function to use for summarizing dataframes."""
    return DataFrameSummarizer.instance().summarizing_func


def set_summarizing_function(func: Callable) -> None:
    """Set the function to use for summarizing dataframes."""
    DataFrameSummarizer.instance().summarizing_func = func


def make_df_summary(df: pd.DataFrame) -> str:
    """Generate a summary of a dataframe using the configured summarizing_func."""
    return DataFrameSummarizer.instance().summarize(df)
