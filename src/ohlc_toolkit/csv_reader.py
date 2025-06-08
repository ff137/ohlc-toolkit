"""Module for loading OHLC data from a CSV file."""

import pandas as pd

from ohlc_toolkit.config import DEFAULT_COLUMNS, DEFAULT_DTYPE
from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.timeframes import (
    parse_timeframe,
    validate_timeframe,
    validate_timeframe_format,
)
from ohlc_toolkit.utils import check_data_integrity, infer_time_step

LOGGER = get_logger(__name__)


def read_ohlc_csv(
    filepath: str,
    timeframe: str | None = None,
    *,
    header_row: int | None = None,
    columns: list[str] | None = None,
    dtype: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Read OHLC data from a CSV file.

    Arguments:
        filepath (str): Path to the CSV file.
        timeframe (Optional[str]): User-defined timeframe (e.g., '1m', '5m', '1h').
        header_row (Optional[int]): The row number to use as the header.
        columns (Optional[list[str]]): The expected columns in the CSV file.
        dtype (Optional[dict[str, str]]): The data type for the columns.

    Returns:
        pd.DataFrame: Processed OHLC dataset.

    """
    bound_logger = LOGGER.bind(body=filepath)
    bound_logger.info("Reading OHLC data")

    columns = columns or DEFAULT_COLUMNS
    dtype = dtype or DEFAULT_DTYPE

    read_csv_params = {
        "filepath_or_buffer": filepath,
        "names": columns,
        "dtype": dtype,
    }

    if ".gz" in filepath:
        read_csv_params["compression"] = "gzip"

    def _read_csv(header: int | None = None) -> pd.DataFrame:
        return pd.read_csv(**read_csv_params, header=header)

    # If header_row is provided, use it directly
    if header_row is not None:
        df = _read_csv(header=header_row)
    else:
        # User doesn't specify header - let's try reading without header first
        try:
            bound_logger.debug("Trying to read file without header")
            df = _read_csv(header=None)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {filepath}") from e
        except ValueError:
            # If that fails, try with header
            bound_logger.debug("Trying to read file with header")
            try:
                df = _read_csv(header=0)
            except ValueError as e:
                raise ValueError(
                    f"Data for file {filepath} does not match expected schema. "
                    f"Please validate the file data aligns with the expected "
                    f"columns ({columns}) and data types ({dtype})"
                ) from e

    bound_logger.debug(
        "Read {} rows and {} columns: {}", df.shape[0], df.shape[1], df.columns.tolist()
    )

    # Infer time step from data
    time_step_seconds = infer_time_step(df, logger=bound_logger)

    # Convert user-defined timeframe to seconds
    timeframe_seconds = None
    if timeframe:
        if not validate_timeframe_format(timeframe):
            raise ValueError(f"Invalid timeframe format: {timeframe}")

        timeframe_seconds = parse_timeframe(timeframe)

        validate_timeframe(time_step_seconds, timeframe_seconds, bound_logger)

    df = df.sort_values("timestamp")  # Ensure timestamp is sorted

    # Perform integrity checks
    check_data_integrity(df, logger=bound_logger, time_step_seconds=time_step_seconds)

    # Convert the timestamp column to a datetime index
    df.index = pd.to_datetime(df["timestamp"], unit="s")
    df.index.name = "datetime"

    bound_logger.info("OHLC data successfully loaded.")
    return df
