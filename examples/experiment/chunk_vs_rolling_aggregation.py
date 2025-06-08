"""Experimental script to compare runtime of rolling window vs chunk-aggregation methods for aggregating OHLC data.

Results show that chunk-based aggregation may be faster when the number of chunks is less than 18000.
"""

import random
import timeit

import pandas as pd

from ohlc_toolkit import read_ohlc_csv
from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.transform import rolling_ohlc

logger = get_logger(__name__)
# Load the sample dataset
df_1min = read_ohlc_csv("data/btcusd_bitstamp_1min_latest.csv", timeframe="1m")

# Define the parameters for the test
timeframe = "1w"
timeframe_minutes = 10080
step_sizes = [3, 4, 5, 6, 10, 15]


def chunk_based_aggregation(df, timeframe_minutes, step_size_minutes):
    """Perform chunk-based aggregation."""
    logger.debug(
        "Chunk-based aggregation: {}, {}. {} chunks",
        timeframe_minutes,
        step_size_minutes,
        len(df) / step_size_minutes,
    )
    aggregated_data = []
    for start in range(0, len(df), step_size_minutes):
        end = start + timeframe_minutes
        if end > len(df):
            break

        window_df = df.iloc[start:end]
        aggregated_row = {
            "timestamp": window_df.index[-1],
            "open": window_df["open"].iloc[0],
            "high": window_df["high"].max(),
            "low": window_df["low"].min(),
            "close": window_df["close"].iloc[-1],
            "volume": window_df["volume"].sum(),
        }
        aggregated_data.append(aggregated_row)
    return pd.DataFrame(aggregated_data)


def test_rolling_aggregation(step_size):
    """Test the rolling aggregation method."""
    df_agg = rolling_ohlc(df_1min, timeframe_minutes)
    df_agg = df_agg.iloc[::step_size]


def test_chunk_aggregation(step_size):
    """Test the chunk-based aggregation method."""
    chunk_based_aggregation(df_1min, timeframe_minutes, step_size)


# Run the performance tests
rolling_time = (
    timeit.timeit(lambda: test_rolling_aggregation(random.choice(step_sizes)), number=5)
    / 5
)
for step_size in step_sizes:
    chunk_time = timeit.timeit(lambda: test_chunk_aggregation(step_size), number=3) / 3  # noqa: B023

    print(f"Step size: {step_size} minutes")
    print(f"Rolling aggregation time: {rolling_time:.4f} seconds")
    print(f"Chunk-based aggregation time: {chunk_time:.4f} seconds")
    print("-" * 40)
