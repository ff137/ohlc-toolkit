"""Transform OHLC data."""

from logging import Logger
from typing import Union

import pandas as pd

from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.timeframes import parse_timeframe, validate_timeframe
from ohlc_toolkit.utils import check_data_integrity

LOGGER = get_logger(__name__)


def _first(row: pd.Series) -> float:
    """Get the first value of a row, for rolling_ohlc aggregation."""
    return row.iloc[0]


def _last(row: pd.Series) -> float:
    """Get the last value of a row, for rolling_ohlc aggregation."""
    return row.iloc[-1]


def rolling_ohlc(df_input: pd.DataFrame, timeframe_minutes: int) -> pd.DataFrame:
    """Rolling OHLC aggregation.

    Args:
        df_input (pd.DataFrame): The input DataFrame with OHLC data.
        timeframe_minutes (int): The timeframe in minutes for the rolling window.

    Returns:
        pd.DataFrame: The aggregated OHLC data, with same schema as the input DataFrame.
    """
    LOGGER.info("Computing OHLC for a rolling window of {} minutes", timeframe_minutes)
    return df_input.rolling(timeframe_minutes).agg(
        {
            "timestamp": _last,
            "open": _first,
            "high": "max",
            "low": "min",
            "close": _last,
            "volume": "sum",
        }
    )


def _cast_to_original_dtypes(
    original_df: pd.DataFrame, transformed_df: pd.DataFrame
) -> pd.DataFrame:
    """Cast the transformed DataFrame to the original DataFrame's data types.

    Args:
        original_df (pd.DataFrame): The original DataFrame with the desired data types.
        transformed_df (pd.DataFrame): The transformed DataFrame to be cast.

    Returns:
        pd.DataFrame: The transformed DataFrame with data types matching the original.
    """
    LOGGER.debug("Resampled DataFrame after casting to original dtypes")
    for column in transformed_df.columns:
        if column in original_df.columns:
            transformed_df[column] = transformed_df[column].astype(
                original_df[column].dtype
            )
    return transformed_df


def _drop_expected_nans(df: pd.DataFrame, logger: Logger) -> pd.DataFrame:
    """Drop the expected NaNs from the DataFrame.

    We expect the first `timeframe_minutes - 1` rows to be NaNs from the aggregation.
    However, we don't want to drop all NaNs in case there are unexpected ones.
    Therefore, we drop the expected NaNs and proceed with data integrity checks.

    Args:
        df (pd.DataFrame): The DataFrame to drop NaNs from.
        logger (Logger): The logger to use.

    Returns:
        pd.DataFrame: The DataFrame with expected NaNs dropped.
    """
    logger.debug("Dropping expected NaN values from the aggregated DataFrame")
    n = df.first_valid_index()  # Get the index of the first valid row
    if n is None:
        logger.error("No valid rows after aggregation.")
        raise ValueError("No valid rows after aggregation.")

    n_pos = df.index.get_loc(n)
    return pd.concat([df.iloc[:n_pos].dropna(), df.iloc[n_pos:]])


def transform_ohlc(
    df_input: pd.DataFrame, timeframe: Union[int, str], step_size_minutes: int = 1
) -> pd.DataFrame:
    """Transform OHLC data to a different timeframe resolution.

    Args:
        df_input (pd.DataFrame): Input DataFrame with OHLC data.
        timeframe (Union[int, str]): Desired timeframe resolution, which can be
            an integer (in minutes) or a string (e.g., '1h', '4h30m').
        step_size_minutes (int): Step size in minutes for the rolling window.

    Returns:
        pd.DataFrame: Transformed OHLC data.
    """
    df = df_input.copy()
    bound_logger = LOGGER.bind(
        body={"timeframe": timeframe, "step_size": step_size_minutes}
    )
    bound_logger.debug("Starting transformation of OHLC data")

    # Convert string timeframe to minutes if necessary
    if isinstance(timeframe, str):
        timeframe_seconds = parse_timeframe(timeframe)
        bound_logger.debug("Parsed timeframe string to seconds: {}", timeframe_seconds)
        if timeframe_seconds % 60 != 0:
            bound_logger.error("Second-level timeframes are not yet supported.")
            raise NotImplementedError("Second-level timeframes are not yet supported.")
        timeframe_minutes = int(timeframe_seconds / 60)
    elif isinstance(timeframe, int):
        timeframe_minutes = timeframe
    else:
        bound_logger.error("Invalid timeframe provided: {}", timeframe)
        raise ValueError(f"Invalid timeframe: {timeframe}")

    time_step_seconds = step_size_minutes * 60
    validate_timeframe(
        time_step=time_step_seconds,
        user_timeframe=timeframe_minutes * 60,
        logger=bound_logger,
    )

    bound_logger.debug(
        "Using timeframe of {} minutes for rolling aggregation", timeframe_minutes
    )

    # Do a check to ensure index of dataframe is a datetime index
    if not pd.api.types.is_datetime64_any_dtype(df_input.index):
        bound_logger.debug(
            "DataFrame index is not a datetime index, sorting by timestamp"
        )
        df = df.sort_values("timestamp")  # Ensure timestamp is sorted

        # Convert the timestamp column to a datetime index
        df.index = pd.to_datetime(df["timestamp"], unit="s")
        df.index.name = "datetime"
        bound_logger.debug("Converted timestamp column to datetime index")

    # Resample the data using the rolling_ohlc function
    df_agg = rolling_ohlc(df, timeframe_minutes)

    # Drop the expected NaNs
    try:
        df_agg = _drop_expected_nans(df_agg, bound_logger)
    except ValueError as e:
        raise ValueError(
            f"{str(e)} Please ensure your dataset is big enough "
            f"for this timeframe: {timeframe} ({timeframe_minutes} minutes)."
        ) from e

    # Cast the transformed DataFrame to the original DataFrame's data types
    df_agg = _cast_to_original_dtypes(df_input, df_agg)

    # Select every step_size-th row from the aggregated DataFrame
    df_agg = df_agg.iloc[::step_size_minutes]

    check_data_integrity(
        df_agg, logger=bound_logger, time_step_seconds=time_step_seconds
    )

    return df_agg
