"""This script demonstrates basic functionality of `ohlc-toolkit`."""

import ohlc_toolkit

df_1min = ohlc_toolkit.read_ohlc_csv(
    "data/btcusd_bitstamp_1min_latest.csv", timeframe="1m"
)

print("Input 1-minute OHLC data:\n")
print(df_1min)


df_5min = ohlc_toolkit.transform_ohlc(df_1min, timeframe=5)  # int timeframe supported

print("Transformed 5-minute OHLC data (updated every minute):\n")
print(df_5min)


df_1h = ohlc_toolkit.transform_ohlc(df_1min, timeframe="1h", step_size_minutes=10)

print("Transformed 1-hour OHLC data (updated every 10 minutes):\n")
print(df_1h)


df_arb = ohlc_toolkit.transform_ohlc(df_1min, timeframe="1d2h3m", step_size_minutes=137)

print("Arbitrary timeframe (1 day 2 hours 3 minutes) with step size 137 minutes:\n")
print(df_arb)
