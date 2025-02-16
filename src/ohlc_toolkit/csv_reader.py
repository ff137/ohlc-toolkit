"""Module for loading OHLC data from a CSV file."""

from typing import Optional

import pandas as pd

from ohlc_toolkit.config import EXPECTED_COLUMNS
from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.timeframes import (
    parse_timeframe,
    validate_timeframe,
    validate_timeframe_format,
)
from ohlc_toolkit.utils import check_data_integrity, infer_time_step

logger = get_logger(__name__)


def read_ohlc_csv(
    filepath: str,
    timeframe: Optional[str] = None,
    expected_columns: Optional[list[str]] = None,
    header_row: Optional[int] = None,
    dtype: Optional[dict[str, str]] = None,
) -> pd.DataFrame:
    """Read OHLC data from a CSV file.

    Arguments:
        filepath (str): Path to the CSV file.
        timeframe (Optional[str]): User-defined timeframe (e.g., '1m', '5m', '1h').
        expected_columns (Optional[list[str]]): The expected columns in the CSV file.
        header_row (Optional[int]): The row number to use as the header.
        dtype (Optional[dict[str, str]]): The data type for the columns.

    Returns:
        pd.DataFrame: Processed OHLC dataset.
    """
    bound_logger = logger.bind(body=filepath)
    bound_logger.info("Reading OHLC data")

    if expected_columns is None:
        expected_columns = EXPECTED_COLUMNS
    if dtype is None:
        dtype = {"timestamp": "int32"}

    read_csv_params = {
        "filepath_or_buffer": filepath,
        "names": expected_columns,
        "dtype": dtype,
    }

    # If header_row is provided, use it directly
    if header_row is not None:
        df = pd.read_csv(**read_csv_params, header=header_row)
    else:
        # User doesn't specify header - let's try reading without header first
        try:
            df = pd.read_csv(**read_csv_params, header=None)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except ValueError:
            # If that fails, try with header
            df = pd.read_csv(**read_csv_params, header=0)

    bound_logger.debug(
        f"Read {df.shape[0]} rows and {df.shape[1]} columns: {df.columns.tolist()}"
    )

    # Infer time step from data
    time_step = infer_time_step(df)

    # Convert user-defined timeframe to seconds
    timeframe_seconds = None
    if timeframe:
        if not validate_timeframe_format(timeframe):
            raise ValueError(f"Invalid timeframe format: {timeframe}")

        timeframe_seconds = parse_timeframe(timeframe)

        validate_timeframe(time_step, timeframe_seconds, bound_logger)

    # Perform integrity checks
    check_data_integrity(df, time_step)

    bound_logger.info("OHLC data successfully loaded.")
    return df
