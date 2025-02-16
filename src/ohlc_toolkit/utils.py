"""This module contains utility functions for the OHLC toolkit."""

from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger


def infer_time_step(df: pd.DataFrame) -> int:
    """Infer the time step by analyzing the timestamp column."""
    time_diffs = np.diff(df["timestamp"])

    if len(time_diffs) == 0:
        raise ValueError("Cannot infer time step from a single-row dataset.")

    time_step = int(pd.Series(time_diffs).mode()[0])  # Most frequent difference
    logger.info(f"Inferred time step: {time_step} seconds")
    return time_step


def check_data_integrity(df: pd.DataFrame, time_step: Optional[int] = None):
    """Perform basic data integrity checks on the OHLC dataset."""
    if df.isnull().values.any():
        logger.warning("Data contains null values.")

    if df["timestamp"].duplicated().any():
        logger.warning("Duplicate timestamps found in the dataset.")

    if time_step:
        expected_timestamps = set(
            range(df["timestamp"].min(), df["timestamp"].max() + time_step, time_step)
        )
        actual_timestamps = set(df["timestamp"])
        missing_timestamps = expected_timestamps - actual_timestamps

        if missing_timestamps:
            logger.warning(f"Missing {len(missing_timestamps)} timestamps in dataset.")
