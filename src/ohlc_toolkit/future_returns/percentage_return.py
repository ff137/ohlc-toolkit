"""Functions for calculating percentage returns."""

import pandas as pd

from ohlc_toolkit.pandas_ta.percent_return import percent_return


def calculate_percentage_return(  # noqa: PLR0913
    close: pd.Series,
    *,
    timestep_size: int,
    future_return_length: int,
    cumulative: bool = False,
    offset: int = 0,
    fillna: object = None,
) -> pd.Series:
    """Calculate the percentage return of a series with customizable options.

    Args:
        close (pd.Series): Series of 'close' prices.
        timestep_size (int): The size of each timestep in minutes.
        future_return_length (int): The desired future return length in minutes.
        cumulative (bool): If True, returns the cumulative returns. Default is False.
        offset (int): How many periods to offset the result. Default is 0.
        fillna (object, optional): Value to fill NaN values with. Default is None.

    Returns:
        pd.Series: The calculated percentage return.

    """
    # Calculate the length for percent return
    length = future_return_length // timestep_size

    # Calculate the percentage return
    pct_return = percent_return(
        close=close,
        length=length,
        cumulative=cumulative,
        offset=offset,
        fillna=fillna,
    )

    return pct_return
