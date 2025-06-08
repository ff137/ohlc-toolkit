"""Functions for loading OHLC data from a CSV file."""

import os

import pandas as pd
import requests
from tqdm import tqdm

from ohlc_toolkit.config.log_config import get_logger

LOGGER = get_logger(__name__)


class BitstampDatasetDownloader:
    """Class for downloading Bitstamp datasets from https://github.com/ff137/bitstamp-btcusd-minute-data."""

    def __init__(self, data_dir: str = "data"):
        """Initialize the Bitstamp dataset downloader."""
        self.data_dir = data_dir.rstrip("/")

        self.DATA_BASE_URL = "https://raw.githubusercontent.com/ff137/bitstamp-btcusd-minute-data/main/data"
        self.BITSTAMP_BULK_DATA_URL = (
            f"{self.DATA_BASE_URL}/historical/btcusd_bitstamp_1min_2012-2025.csv.gz"
        )
        self.BITSTAMP_RECENT_DATA_URL = (
            f"{self.DATA_BASE_URL}/updates/btcusd_bitstamp_1min_latest.csv"
        )

    def _download_file(self, url: str, output_path: str):
        """Download a file from a URL with a progress bar."""
        LOGGER.info("Initializing download of file from `{}`", url)
        response = requests.get(url, stream=True, allow_redirects=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte

        with (
            open(output_path, "wb") as file,
            tqdm(
                desc=output_path,
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar,
        ):
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))

        # Get the actual file size using tqdm's n attribute
        file_size_mb = progress_bar.n / (1024 * 1024)  # Convert to MB
        LOGGER.info(
            "Successfully downloaded file to `{}` ({:.2f} MB)",
            output_path,
            file_size_mb,
        )

    def download_bitstamp_btcusd_minute_data(
        self,
        *,
        bulk: bool = False,
        recent: bool = True,
        overwrite_bulk: bool = False,
        overwrite_recent: bool = True,
        skip_read: bool = False,
    ) -> pd.DataFrame | None:
        """Download the Bitstamp BTC/USD minute datasets.

        Args:
            bulk: Whether to download the bulk dataset. Default is to skip bulk dataset.
            recent: Whether to download the recent dataset. Default is True.
            overwrite_bulk: Whether to overwrite the existing bulk dataset. By default
                will not overwrite bulk data if it already exists.
            overwrite_recent: Whether to overwrite the existing recent dataset. By default
                will overwrite recent data if it already exists.
            skip_read: Whether to skip reading the downloaded datasets into DataFrames.
                Default behaviour will read and return the DataFrames.

        Returns:
            pd.DataFrame: If skip_read = False, the downloaded datasets, merged if both
                are requested. If skip_read = True, None is returned.

        """
        if not (bulk or recent):
            raise ValueError("At least one of 'bulk' or 'recent' must be True.")
        dataframes = []

        if bulk:
            bulk_file_name = self.BITSTAMP_BULK_DATA_URL.split("/")[-1]
            bulk_file_path = f"{self.data_dir}/{bulk_file_name}"

            # check if the file already exists
            if os.path.exists(bulk_file_path) and not overwrite_bulk:
                LOGGER.info("Bulk dataset already exists, skipping download")
                df_bulk = pd.read_csv(bulk_file_path, compression="gzip")
                dataframes.append(df_bulk)
            else:
                LOGGER.info("Downloading bulk dataset")
                self._download_file(self.BITSTAMP_BULK_DATA_URL, bulk_file_path)

            if not skip_read:
                LOGGER.info("Reading bulk dataset into DataFrame")
                df_bulk = pd.read_csv(bulk_file_path, compression="gzip")
                dataframes.append(df_bulk)

        if recent:
            recent_file_name = self.BITSTAMP_RECENT_DATA_URL.split("/")[-1]
            recent_file_path = f"{self.data_dir}/{recent_file_name}"

            # check if the file already exists
            if os.path.exists(recent_file_path) and not overwrite_recent:
                LOGGER.info("Recent dataset already exists, skipping download")
                df_recent = pd.read_csv(recent_file_path)
                dataframes.append(df_recent)
            else:
                LOGGER.info("Downloading recent dataset")
                self._download_file(self.BITSTAMP_RECENT_DATA_URL, recent_file_path)

            if not skip_read:
                LOGGER.info("Reading recent dataset into DataFrame")
                df_recent = pd.read_csv(recent_file_path)
                dataframes.append(df_recent)

        return pd.concat(dataframes) if dataframes else None

    def download_all_bitstamp_btcusd_minute_data(
        self,
        *,
        overwrite_bulk: bool = False,
        overwrite_recent: bool = True,
    ) -> pd.DataFrame:
        """Download all Bitstamp BTC/USD minute datasets.

        Args:
            overwrite_bulk: Whether to overwrite the existing bulk dataset.
            overwrite_recent: Whether to overwrite the existing recent dataset.

        Returns:
            pd.DataFrame: The downloaded datasets.

        """
        return self.download_bitstamp_btcusd_minute_data(
            bulk=True,
            recent=True,
            overwrite_bulk=overwrite_bulk,
            overwrite_recent=overwrite_recent,
        )
