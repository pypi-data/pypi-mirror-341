"""Predefined library of Data Integration and Summarization steps for data processing."""

from typing import Callable, Dict, List

import pandas as pd


def group_and_aggregate(
    data: pd.DataFrame, group_by_columns: List[str], agg_funcs: Dict[str, Callable]
) -> pd.DataFrame:
    """
    Group data by specified columns and apply aggregation functions.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame.
    group_by_columns : List[str]
        Columns to group by.
    agg_funcs : Dict[str, Callable]
        Dictionary mapping column names to aggregation functions.

    Returns
    -------
    pd.DataFrame
        Aggregated DataFrame.
    """
    return data.groupby(group_by_columns).agg(agg_funcs).reset_index()
