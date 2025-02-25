"""Test cases for the utils module."""

import unittest

import pandas as pd

from ohlc_toolkit.config.log_config import get_logger
from ohlc_toolkit.utils import check_data_integrity, infer_time_step


class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    def setUp(self):
        """Set up test data."""
        self.logger = get_logger(__name__)
        self.df_valid = pd.DataFrame(
            {
                "timestamp": [
                    1609459200,
                    1609459260,
                    1609459320,
                    1609459380,
                ],  # 1-minute intervals
                "open": [1, 2, 3, 4],
                "high": [2, 3, 4, 5],
                "low": [0, 1, 2, 3],
                "close": [1.5, 2.5, 3.5, 4.5],
                "volume": [100, 200, 300, 400],
            }
        )

        self.df_single_row = pd.DataFrame(
            {
                "timestamp": [1609459200],
                "open": [1],
                "high": [2],
                "low": [0],
                "close": [1.5],
                "volume": [100],
            }
        )

        self.df_with_nulls = self.df_valid.copy()
        self.df_with_nulls.loc[1, "close"] = None

        self.df_with_duplicates = self.df_valid.copy()
        self.df_with_duplicates.loc[1, "timestamp"] = 1609459200

    def test_infer_time_step(self):
        """Test inferring time step."""
        self.assertEqual(infer_time_step(self.df_valid, self.logger), 60)

        with self.assertRaises(ValueError):
            infer_time_step(self.df_single_row, self.logger)

    def test_infer_time_step_invalid_timestamp_type(self):
        """Test inferring time step with invalid timestamp type."""
        df_invalid_timestamp_type = self.df_valid.copy()
        df_invalid_timestamp_type["timestamp"] = df_invalid_timestamp_type[
            "timestamp"
        ].astype(str)
        with self.assertRaises(TypeError) as context:
            infer_time_step(df_invalid_timestamp_type, self.logger)
        self.assertEqual(
            str(context.exception),
            "The provided timestamp column contains non-numeric values. "
            "All values must be UNIX timestamps (seconds since epoch).",
        )

    def test_infer_time_step_missing_timestamp_column(self):
        """Test inferring time step with missing timestamp column."""
        df_missing_timestamp_column = self.df_valid.drop(columns=["timestamp"])
        with self.assertRaises(KeyError) as context:
            infer_time_step(df_missing_timestamp_column, self.logger)
        self.assertEqual(
            str(context.exception), "'Timestamp column not found in DataFrame.'"
        )

    def test_check_data_integrity(self):
        """Test checking data integrity."""
        # No warnings expected
        check_data_integrity(self.df_valid, self.logger, 60)

        # Check for null values
        check_data_integrity(self.df_with_nulls, self.logger, 60)

        # Check for duplicate timestamps
        check_data_integrity(self.df_with_duplicates, self.logger, 60)

        # Check for missing timestamps
        df_missing_timestamps = self.df_valid.drop(2)
        check_data_integrity(df_missing_timestamps, self.logger, 60)


if __name__ == "__main__":
    unittest.main()
