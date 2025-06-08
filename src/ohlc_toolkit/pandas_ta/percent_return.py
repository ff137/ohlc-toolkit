"""Percent Return from pandas-ta."""

from numpy import nan, roll
from pandas import Series

from ohlc_toolkit.pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series


def percent_return(
    close: Series,
    length: int | None = None,
    cumulative: bool | None = None,
    offset: int | None = None,
    fillna: str | None = None,
) -> Series:
    """Percent Return.

    Calculates the percent return of a Series.
    See also: help(df.ta.percent_return) for additional **kwargs a valid 'df'.

    Sources:
        https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

    Args:
        close (pd.Series): Series of 'close's
        length (int): Its period. Default: 1
        cumulative (bool): If True, returns the cumulative returns.
            Default: False
        offset (int): How many periods to offset the result. Default: 0
        fillna (object, optional): Value to fill NaN values with. Default is None.

    Returns:
        pd.Series: New feature generated.

    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length + 1)

    if close is None:
        raise ValueError(
            "Series length does not meet the minimum length required for the indicator."
        )

    cumulative = v_bool(cumulative, False)
    offset = v_offset(offset)

    # Calculate
    np_close = close.to_numpy()
    if cumulative:
        pr = (np_close / np_close[0]) - 1
    else:
        pr = (np_close / roll(np_close, length)) - 1
        pr[:length] = nan
    pct_return = Series(pr, index=close.index)

    # Offset
    if offset != 0:
        pct_return = pct_return.shift(offset)

    # Fill
    if fillna is not None:
        pct_return.fillna(fillna, inplace=True)

    # Name and Category
    pct_return.name = f"{'CUM' if cumulative else ''}PCTRET_{length}"
    pct_return.category = "performance"

    return pct_return
