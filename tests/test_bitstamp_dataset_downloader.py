"""Tests for the BitstampDatasetDownloader class."""

import unittest
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from ohlc_toolkit.bitstamp_dataset_downloader import BitstampDatasetDownloader


class TestBitstampDatasetDownloader(unittest.TestCase):
    """Tests for the BitstampDatasetDownloader class."""

    def setUp(self):
        """Set up the test case."""
        self.downloader = BitstampDatasetDownloader(data_dir="test_data")

    @patch("ohlc_toolkit.bitstamp_dataset_downloader.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_download_recent_data(self, mock_exists, mock_open, mock_get):
        """Test downloading recent data."""
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"data"]
        mock_response.headers = {"content-length": "4"}
        mock_get.return_value = mock_response

        # Mock os.path.exists to simulate file not existing
        mock_exists.return_value = False

        # Call the method
        with patch("pandas.read_csv", return_value=pd.DataFrame()):
            df = self.downloader.download_bitstamp_btcusd_minute_data(
                recent=True, bulk=False
            )

        # Assertions
        mock_get.assert_called_once_with(
            "https://raw.githubusercontent.com/ff137/bitstamp-btcusd-minute-data/"
            "main/data/updates/btcusd_bitstamp_1min_latest.csv",
            stream=True,
            allow_redirects=True,
        )
        mock_open.assert_called_once_with(
            "test_data/btcusd_bitstamp_1min_latest.csv", "wb"
        )
        self.assertIsInstance(df, pd.DataFrame)

    @patch("ohlc_toolkit.bitstamp_dataset_downloader.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_download_bulk_data(self, mock_exists, mock_open, mock_get):
        """Test downloading bulk data."""
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"data"]
        mock_response.headers = {"content-length": "4"}
        mock_get.return_value = mock_response

        # Mock os.path.exists to simulate file not existing
        mock_exists.return_value = False

        # Call the method
        with patch("pandas.read_csv", return_value=pd.DataFrame()):
            df = self.downloader.download_bitstamp_btcusd_minute_data(
                bulk=True, recent=False
            )

        # Assertions
        mock_get.assert_called_once_with(
            "https://raw.githubusercontent.com/ff137/bitstamp-btcusd-minute-data/"
            "main/data/historical/btcusd_bitstamp_1min_2012-2025.csv.gz",
            stream=True,
            allow_redirects=True,
        )
        mock_open.assert_called_once_with(
            "test_data/btcusd_bitstamp_1min_2012-2025.csv.gz", "wb"
        )
        self.assertIsInstance(df, pd.DataFrame)

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_csv", return_value=pd.DataFrame())
    def test_skip_download_if_exists(self, mock_read_csv, mock_exists):
        """Test skipping download if file exists."""
        # Call the method
        df = self.downloader.download_bitstamp_btcusd_minute_data(
            bulk=True, recent=True, overwrite_bulk=False, overwrite_recent=False
        )

        # Assertions
        mock_read_csv.assert_any_call(
            "test_data/btcusd_bitstamp_1min_2012-2025.csv.gz", compression="gzip"
        )
        mock_read_csv.assert_any_call("test_data/btcusd_bitstamp_1min_latest.csv")
        self.assertIsInstance(df, pd.DataFrame)

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_csv", return_value=pd.DataFrame())
    def test_download_all_bitstamp_btcusd_minute_data(self, mock_read_csv, mock_exists):
        """Test the download_all_bitstamp_btcusd_minute_data method."""
        # Call the method
        df = self.downloader.download_all_bitstamp_btcusd_minute_data(
            overwrite_bulk=False, overwrite_recent=False
        )

        # Assertions
        mock_read_csv.assert_any_call(
            "test_data/btcusd_bitstamp_1min_2012-2025.csv.gz", compression="gzip"
        )
        mock_read_csv.assert_any_call("test_data/btcusd_bitstamp_1min_latest.csv")
        self.assertIsInstance(df, pd.DataFrame)

    def test_bad_download_request(self):
        """Test exception raised on neither bulk nor recent requested."""
        with self.assertRaises(ValueError):
            self.downloader.download_bitstamp_btcusd_minute_data(
                bulk=False, recent=False
            )


if __name__ == "__main__":
    unittest.main()
