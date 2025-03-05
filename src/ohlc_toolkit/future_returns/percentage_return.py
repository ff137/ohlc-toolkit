"""This module contains functions for calculating percentage returns."""

from typing import Literal, Optional

import pandas as pd
import pandas_ta as ta


def calculate_percentage_return(
    close: pd.Series,
    *,
    timestep_size: int,
    future_return_length: int,
    cumulative: bool = False,
    offset: int = 0,
    fillna: object = None,
    fill_method: Optional[Literal["bfill", "ffill"]] = None,
) -> pd.Series:
    """Calculate the percentage return of a series with customizable options.

    Args:
        close (pd.Series): Series of 'close' prices.
        timestep_size (int): The size of each timestep in minutes.
        future_return_length (int): The desired future return length in minutes.
        cumulative (bool): If True, returns the cumulative returns. Default is False.
        offset (int): How many periods to offset the result. Default is 0.
        fillna (object, optional): Value to fill NaN values with. Default is None.
        fill_method (str, optional): Method to use for filling holes in re-indexed Series:
            * ffill: Forward fill - propagate last valid observation forward to next valid.
            * bfill: Backward fill - use next valid observation to fill gap.
            Default is None.

    Returns:
        pd.Series: The calculated percentage return.
    """
    # Calculate the length for percent return
    length = future_return_length // timestep_size

    # Calculate the percentage return using pandas_ta
    pct_return = ta.percent_return(
        close=close,
        length=length,
        cumulative=cumulative,
        offset=offset,
        fillna=fillna,
        fill_method=fill_method,
    )

    return pct_return
