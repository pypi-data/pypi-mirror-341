"""
This module contains preprocessing steps for pandas dataframes.

Functions:
    - remove_duplicates: Removes duplicate rows from a dataframe.
    - fill_missing_values: Fills missing values in a dataframe with specified values.
    - make_columns_snake_case: Converts column names in a dataframe to snake case.
    - select_columns: Selects specific columns from a dataframe.
    - filter_rows: Filters rows in a dataframe based on specified conditions.
    - scale_data: Scales the values in a dataframe to a specified range.
    - encode_categorical: Encodes categorical variables in a dataframe.
    - divide_one_column_by_another: Divides the values in one column of a dataframe by the values in another column.
    - merge_with: Merges two dataframes based on specified columns.
    - group_and_aggregate: Groups rows in a dataframe and performs aggregation on specified columns.
"""

from .clean import fill_missing_values, make_columns_snake_case, remove_duplicates
from .combine import group_and_aggregate
from .filter import filter_rows, select_columns
from .transform import divide_one_column_by_another, encode_categorical, scale_data
from .validate import validate_is_dataframe

__all__ = [
    # clean.py
    "remove_duplicates",
    "fill_missing_values",
    "make_columns_snake_case",
    # filter.py
    "select_columns",
    "filter_rows",
    # transform.py
    "scale_data",
    "encode_categorical",
    "divide_one_column_by_another",
    # combine.py
    "group_and_aggregate",
    # validate.py
    "validate_is_dataframe",
]
