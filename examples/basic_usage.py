"""This script demonstrates basic functionality of `ohlc-toolkit`."""

import ohlc_toolkit

df = ohlc_toolkit.read_ohlc_csv("data/btcusd_bitstamp_1min_latest.csv", timeframe="1m")

print(df)
