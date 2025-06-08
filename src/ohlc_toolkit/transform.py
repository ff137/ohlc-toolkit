"""Transform OHLC data."""

import os
from logging import Logger

import pandas as pd

from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.exceptions import DatasetEmptyError
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
    """Apply rolling OHLC aggregation.

    Args:
        df_input (pd.DataFrame): The input DataFrame with OHLC data.
        timeframe_minutes (int): The timeframe in minutes for the rolling window.

    Returns:
        pd.DataFrame: The aggregated OHLC data, with same schema as the input DataFrame.

    """
    LOGGER.info(
        "Calculating OHLC using a {}-minute rolling window over {} rows.",
        timeframe_minutes,
        len(df_input),
    )
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
    LOGGER.debug("Casting transformed DataFrame to original dtypes")
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
        raise DatasetEmptyError("No valid rows after aggregation.")

    n_pos = df.index.get_loc(n)

    result = pd.concat([df.iloc[:n_pos].dropna(), df.iloc[n_pos:]])
    return result


def transform_ohlc(
    df_input: pd.DataFrame, timeframe: int | str, step_size_minutes: int = 1
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

    timeframe_minutes = _parse_timeframe_to_minutes(timeframe, bound_logger)
    time_step_seconds = step_size_minutes * 60

    validate_timeframe(
        time_step=time_step_seconds,
        user_timeframe=timeframe_minutes * 60,
        logger=bound_logger,
    )

    # Apply rolling or chunk-based aggregation to transform the data
    df_agg = _aggregate_ohlc_data(
        df, timeframe_minutes, step_size_minutes, bound_logger
    )

    try:
        df_agg = _drop_expected_nans(df_agg, bound_logger)
    except DatasetEmptyError as e:
        raise ValueError(
            f"{e!s} Please ensure your dataset is big enough "
            f"for this timeframe: {timeframe} ({timeframe_minutes} minutes)."
        ) from e

    df_agg = _cast_to_original_dtypes(df_input, df_agg)

    _ensure_datetime_index(df_input, df, bound_logger)

    check_data_integrity(
        df_agg, logger=bound_logger, time_step_seconds=time_step_seconds
    )

    return df_agg


def _parse_timeframe_to_minutes(timeframe: int | str, logger: Logger) -> int:
    """Parse the timeframe to minutes."""
    if isinstance(timeframe, str):
        timeframe_seconds = parse_timeframe(timeframe)
        logger.debug("Parsed timeframe string to seconds: {}", timeframe_seconds)
        if timeframe_seconds % 60 != 0:
            logger.error("Second-level timeframes are not yet supported.")
            raise NotImplementedError("Second-level timeframes are not yet supported.")
        return timeframe_seconds // 60
    elif isinstance(timeframe, int):
        return timeframe
    else:
        logger.error("Invalid timeframe provided: {}", timeframe)
        raise ValueError(f"Invalid timeframe: {timeframe}")


def _aggregate_ohlc_data(
    df: pd.DataFrame, timeframe_minutes: int, step_size_minutes: int, logger: Logger
) -> pd.DataFrame:
    """Aggregate OHLC data using either rolling or chunk-based aggregation."""
    chunk_cut_off = int(os.getenv("CHUNK_CUT_OFF", "18000"))
    num_rows = len(df)
    num_chunks = num_rows // step_size_minutes

    if step_size_minutes == 1 or num_chunks > chunk_cut_off:
        # Use rolling aggregation for small step sizes or large datasets
        logger.debug(
            "Using rolling aggregation for step size: {}. "
            "The number of rows would yield {} chunks",
            step_size_minutes,
            num_chunks,
        )
        df_agg = rolling_ohlc(df, timeframe_minutes)
        df_agg = df_agg.iloc[::step_size_minutes]
    else:
        # Use chunk-based aggregation when data step is large relative to num rows
        logger.info(
            "Performing chunk-based aggregation over {} rows "
            "with a step size of {} minutes ({} chunks).",
            num_rows,
            step_size_minutes,
            num_chunks,
        )
        df_agg = _chunk_based_aggregation(
            df, timeframe_minutes, step_size_minutes, logger
        )

    return df_agg


def _chunk_based_aggregation(
    df: pd.DataFrame, timeframe_minutes: int, step_size_minutes: int, logger: Logger
) -> pd.DataFrame:
    """Perform chunk-based aggregation on the DataFrame."""
    aggregated_data: list[dict[str, float]] = []
    num_rows = len(df)

    for start in range(0, num_rows, step_size_minutes):
        end = start + timeframe_minutes
        if end > num_rows:
            if not aggregated_data:
                logger.error(
                    "Selected timeframe is too large. {} rows are not enough for "
                    "this timeframe: {} ({} minutes).",
                    num_rows,
                    timeframe_minutes,
                    timeframe_minutes,
                )
                raise ValueError(
                    "Timeframe too large. Please ensure your dataset is big enough "
                    f"for this timeframe: {timeframe_minutes} minutes."
                )
            break

        window_df = df.iloc[start:end]
        aggregated_row = {
            "timestamp": window_df["timestamp"].iloc[-1],
            "open": window_df["open"].iloc[0],
            "high": window_df["high"].max(),
            "low": window_df["low"].min(),
            "close": window_df["close"].iloc[-1],
            "volume": window_df["volume"].sum(),
        }
        aggregated_data.append(aggregated_row)

    df_agg = pd.DataFrame(aggregated_data)
    return df_agg.sort_values("timestamp")


def _ensure_datetime_index(df_input: pd.DataFrame, df: pd.DataFrame, logger: Logger):
    """Ensure the DataFrame index is a datetime index."""
    if not pd.api.types.is_datetime64_any_dtype(df_input.index):
        logger.debug("DataFrame index is not a datetime index, sorting by timestamp")
        df.sort_values("timestamp", inplace=True)
        df.index = pd.to_datetime(df["timestamp"], unit="s")
        df.index.name = "datetime"
        logger.debug("Converted timestamp column to datetime index")
