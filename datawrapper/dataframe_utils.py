"""Utilities for working with dataframes across multiple libraries using Narwhals."""

from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Any

import narwhals as nw
from narwhals.typing import IntoDataFrame

if TYPE_CHECKING:
    import pandas as pd


def to_csv(data: IntoDataFrame | list[dict]) -> str | None:
    """
    Convert a dataframe or list of dicts to CSV string format.

    This function supports multiple dataframe libraries (pandas, Polars, PyArrow, etc.)
    via Narwhals, as well as Python's native list of dictionaries.

    Parameters
    ----------
    data : IntoDataFrame | list[dict]
        The data to convert. Can be:
        - Any dataframe type supported by Narwhals (pandas, Polars, PyArrow, etc.)
        - A list of dictionaries

    Returns
    -------
    str | None
        CSV string representation of the data, or None if data is empty.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> to_csv(df)
    'a,b\\n1,3\\n2,4\\n'

    >>> import polars as pl
    >>> df = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> to_csv(df)
    'a,b\\n1,3\\n2,4\\n'
    """
    # Handle list of dicts
    if isinstance(data, list):
        if not data:
            return None
        # Convert to pandas DataFrame first, then use narwhals
        # This avoids the need to import a specific backend
        import pandas as pd

        df = pd.DataFrame(data)
        return nw.from_native(df, eager_only=True).write_csv()

    # Handle dataframe types via narwhals
    try:
        df_nw = nw.from_native(data, eager_only=True)
        if df_nw.is_empty():
            return None
        return df_nw.write_csv()
    except Exception:
        # If narwhals doesn't support it, return None or raise
        return None


def from_csv(csv_data: str | IntoDataFrame) -> pd.DataFrame:
    """
    Parse CSV string into a pandas DataFrame.

    This function is used for deserializing data from the Datawrapper API.
    While the library now supports multiple dataframe types for input,
    we standardize on pandas DataFrames for data returned from the API
    to maintain backward compatibility.

    Parameters
    ----------
    csv_data : str | IntoDataFrame
        The CSV data from the chart data endpoint, or an existing DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame containing the parsed CSV data

    Examples
    --------
    >>> csv_str = "a,b\\n1,3\\n2,4"
    >>> df = from_csv(csv_str)
    >>> isinstance(df, pd.DataFrame)
    True
    """
    import pandas as pd

    # If it's already a DataFrame, convert to pandas-compatible CSV first.
    # This avoids backend-specific optional dependencies (e.g., Polars -> pandas via pyarrow).
    if not isinstance(csv_data, str):
        try:
            df_nw = nw.from_native(csv_data, eager_only=True)
            csv_string = df_nw.write_csv()
            return pd.read_csv(StringIO(csv_string), sep=None, engine="python")
        except Exception:
            # If it's already a pandas DataFrame, just return it
            if isinstance(csv_data, pd.DataFrame):
                return csv_data
            raise

    # Parse CSV string using pandas
    # Use sep=None with engine='python' to auto-detect delimiter (comma or tab)
    return pd.read_csv(StringIO(csv_data), sep=None, engine="python")


def is_empty(data: IntoDataFrame | list[dict]) -> bool:
    """
    Check if dataframe or list of dicts is empty.

    Parameters
    ----------
    data : IntoDataFrame | list[dict]
        The data to check

    Returns
    -------
    bool
        True if the data is empty, False otherwise

    Examples
    --------
    >>> import pandas as pd
    >>> is_empty(pd.DataFrame())
    True
    >>> is_empty(pd.DataFrame({"a": [1]}))
    False
    >>> is_empty([])
    True
    >>> is_empty([{"a": 1}])
    False
    """
    if isinstance(data, list):
        return not bool(data)

    try:
        df_nw = nw.from_native(data, eager_only=True)
        return df_nw.is_empty()
    except Exception:
        # Fallback for unsupported types
        return True


def normalize_dataframe(data: IntoDataFrame | list[dict]) -> IntoDataFrame:
    """
    Normalize input data to a dataframe type.

    This function accepts various input formats and returns a dataframe.
    It maintains the backend of the input dataframe when possible.

    Parameters
    ----------
    data : IntoDataFrame | list[dict]
        The data to normalize

    Returns
    -------
    IntoDataFrame
        A dataframe (the exact type depends on the input)

    Examples
    --------
    >>> import pandas as pd
    >>> data = [{"a": 1}, {"a": 2}]
    >>> df = normalize_dataframe(data)
    >>> isinstance(df, pd.DataFrame)
    True
    """
    if isinstance(data, list):
        import pandas as pd

        return pd.DataFrame(data)

    # If it's already a dataframe, return as-is
    return data
