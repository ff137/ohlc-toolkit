"""Configuration for the ohlc_toolkit package."""

DEFAULT_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

DEFAULT_DTYPE = {
    "timestamp": "int32",
    "open": "float32",
    "high": "float32",
    "low": "float32",
    "close": "float32",
    "volume": "float32",
}
