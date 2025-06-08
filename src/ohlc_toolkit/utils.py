"""Utility functions for the OHLC toolkit."""

from logging import Logger

import numpy as np
import pandas as pd


def infer_time_step(df: pd.DataFrame, logger: Logger) -> int:
    """Infer the time step by analyzing the timestamp column."""
    try:
        time_diffs = np.diff(df["timestamp"])
    except KeyError as e:
        raise KeyError("Timestamp column not found in DataFrame.") from e
    except TypeError as e:
        raise TypeError(
            "The provided timestamp column contains non-numeric values. "
            "All values must be UNIX timestamps (seconds since epoch)."
        ) from e

    if len(time_diffs) == 0:
        raise ValueError("Cannot infer time step from a single-row dataset.")

    time_step = int(pd.Series(time_diffs).mode()[0])  # Most frequent difference
    logger.info("Inferred time step: {} seconds", time_step)
    return time_step


def check_data_integrity(
    df: pd.DataFrame, logger: Logger, time_step_seconds: int | None = None
):
    """Perform basic data integrity checks on the OHLC dataset."""
    if df.isnull().values.any():
        logger.warning("Data contains null values.")

    if df["timestamp"].duplicated().any():
        logger.warning("Duplicate timestamps found in the dataset.")

    if time_step_seconds:
        expected_timestamps = set(
            range(
                df["timestamp"].min(),
                df["timestamp"].max() + time_step_seconds,
                time_step_seconds,
            )
        )
        actual_timestamps = set(df["timestamp"])
        missing_timestamps = expected_timestamps - actual_timestamps

        if missing_timestamps:
            logger.warning(f"Missing {len(missing_timestamps)} timestamps in dataset.")
