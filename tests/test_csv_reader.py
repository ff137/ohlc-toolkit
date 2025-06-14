"""Tests for the ohlc_toolkit.csv_reader module."""

import unittest
from unittest.mock import patch

import pandas as pd

from ohlc_toolkit.config import DEFAULT_COLUMNS, DEFAULT_DTYPE
from ohlc_toolkit.csv_reader import read_ohlc_csv


class TestCsvReader(unittest.TestCase):
    """Test cases for the ohlc_toolkit.csv_reader module."""

    def setUp(self):
        """Set up test data."""
        self.csv_data_no_header_path = "tests/test_data/test_csv_no_header.csv"
        self.csv_data_w_header_path = "tests/test_data/test_csv_w_header.csv"
        self.csv_bad_data_path = "tests/test_data/test_bad_data.csv"
        self.df_expected = pd.DataFrame(
            data={
                "timestamp": pd.Series(
                    [1736208060, 1736208120, 1736208180, 1736208240], dtype="int32"
                ),
                "open": [102228.0, 102214.0, 102214.0, 102214.0],
                "high": [102228.0, 102225.0, 102220.0, 102214.0],
                "low": [102228.0, 102214.0, 102214.0, 102163.0],
                "close": [102228.0, 102215.0, 102220.0, 102163.0],
                "volume": [0.00114705, 0.42548035, 0.24356262, 0.03850259],
            }
        )
        # Cast to the expected, default dtypes:
        self.df_expected = self.df_expected.astype(
            {
                "open": "float32",
                "high": "float32",
                "low": "float32",
                "close": "float32",
                "volume": "float32",
            }
        )
        # Set expected index:
        self.df_expected.index = pd.to_datetime(self.df_expected["timestamp"], unit="s")
        self.df_expected.index.name = "datetime"

    def test_read_ohlc_csv_valid_no_header(self):
        """Test reading a valid OHLC CSV file with no header."""
        df = read_ohlc_csv(self.csv_data_no_header_path)
        pd.testing.assert_frame_equal(df, self.df_expected)

    def test_read_ohlc_csv_valid_header_row_not_specified(self):
        """Test reading a valid OHLC CSV file with header row, but not specified."""
        df = read_ohlc_csv(self.csv_data_w_header_path)
        pd.testing.assert_frame_equal(df, self.df_expected)

    def test_read_ohlc_csv_valid_w_header_row(self):
        """Test reading a valid OHLC CSV file with header row, and it's specified."""
        df = read_ohlc_csv(self.csv_data_w_header_path, header_row=0)
        pd.testing.assert_frame_equal(df, self.df_expected)

    def test_fails_on_bad_path(self):
        """Test fail on reading a file that doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            read_ohlc_csv("tests/test_data/bad_path.csv")

    def test_fails_on_empty_dataframe(self):
        """Test fail on reading an empty dataframe."""
        with self.assertRaises(ValueError):
            read_ohlc_csv(self.csv_data_w_header_path, header_row=5)

    def test_fails_on_bad_data(self):
        """Test fail on reading a dataframe with bad data."""
        with self.assertRaises(ValueError):
            read_ohlc_csv(self.csv_bad_data_path)

    def test_read_ohlc_csv_with_timeframe(self):
        """Test reading a CSV file with a valid timeframe."""
        df = read_ohlc_csv(self.csv_data_no_header_path, timeframe="1m")
        pd.testing.assert_frame_equal(df, self.df_expected)

    def test_read_ohlc_csv_bad_timeframe_value(self):
        """Test reading a CSV file with an invalid timeframe."""
        with self.assertRaises(ValueError) as context:
            read_ohlc_csv(self.csv_data_no_header_path, timeframe="30s")
        self.assertEqual(
            str(context.exception),
            "Requested timeframe (30s) should not be smaller than time step (60s).",
        )

    def test_read_ohlc_csv_invalid_timeframe_format(self):
        """Test reading a CSV file with an invalid timeframe."""
        with self.assertRaises(ValueError) as context:
            read_ohlc_csv(self.csv_data_no_header_path, timeframe="1x")
        self.assertEqual(str(context.exception), "Invalid timeframe format: 1x")

    def test_read_ohlc_csv_non_multiple_timeframe(self):
        """Test reading a CSV file with a non-multiple timeframe."""
        df = read_ohlc_csv(self.csv_data_no_header_path, timeframe="70s")
        pd.testing.assert_frame_equal(df, self.df_expected)

    @patch("pandas.read_csv")
    def test_read_ohlc_csv_with_gzip_compression(self, mock_read_csv):
        """Test reading a CSV file with gzip compression."""
        with patch("ohlc_toolkit.csv_reader.infer_time_step") as mock_infer_time_step:
            read_ohlc_csv("test_csv_data.gz")
            mock_read_csv.assert_called_once_with(
                filepath_or_buffer="test_csv_data.gz",
                names=DEFAULT_COLUMNS,
                dtype=DEFAULT_DTYPE,
                header=None,
                compression="gzip",
            )
        assert mock_infer_time_step.call_count == 1


if __name__ == "__main__":
    unittest.main()
