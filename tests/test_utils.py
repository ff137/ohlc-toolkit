"""Test cases for the utils module."""

import unittest

import pandas as pd

from ohlc_toolkit.utils import check_data_integrity, infer_time_step


class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    def setUp(self):
        """Set up test data."""
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
        self.assertEqual(infer_time_step(self.df_valid), 60)

        with self.assertRaises(ValueError):
            infer_time_step(self.df_single_row)

    def test_check_data_integrity(self):
        """Test checking data integrity."""
        # No warnings expected
        check_data_integrity(self.df_valid, 60)

        # Check for null values
        check_data_integrity(self.df_with_nulls)

        # Check for duplicate timestamps
        check_data_integrity(self.df_with_duplicates)

        # Check for missing timestamps
        df_missing_timestamps = self.df_valid.drop(2)
        check_data_integrity(df_missing_timestamps, 60)


if __name__ == "__main__":
    unittest.main()
