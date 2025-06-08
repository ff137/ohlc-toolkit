"""Example script to demonstrate basic functionality of `ohlc-toolkit`."""

import ohlc_toolkit

## First, download sample data
downloader = ohlc_toolkit.DatasetDownloader()
downloader.download_bitstamp_btcusd_minute_data(
    bulk=False,  # Don't download the bulk dataset
    recent=True,  # Download the recent data
    overwrite_recent=False,  # Skips download if files already exist (set True to overwrite)
    skip_read=True,  # Don't read the data into memory yet (we will read in the next step)
)


## Then, read the data
df_1min = ohlc_toolkit.read_ohlc_csv(
    "data/btcusd_bitstamp_1min_latest.csv", timeframe="1m"
)

print("Input 1-minute OHLC data:\n")
print(df_1min)


## We can transform the 1-minute data to different timeframes
df_5min = ohlc_toolkit.transform_ohlc(df_1min, timeframe=5)  # int timeframe supported

print("Transformed 5-minute OHLC data (updated every minute):\n")
print(df_5min)


## We can also transform the data to different timeframes with custom step size
df_1h = ohlc_toolkit.transform_ohlc(df_1min, timeframe="1h", step_size_minutes=10)

print("Transformed 1-hour OHLC data (updated every 10 minutes):\n")
print(df_1h)


## We can also transform the data to arbitrary timeframes
df_arb = ohlc_toolkit.transform_ohlc(df_1min, timeframe="1d2h3m", step_size_minutes=137)

print("Arbitrary timeframe (1 day 2 hours 3 minutes) with step size 137 minutes:\n")
print(df_arb)
