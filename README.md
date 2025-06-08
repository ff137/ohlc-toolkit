# OHLC Toolkit

[![PyPI](https://img.shields.io/pypi/v/ohlc-toolkit)](https://pypi.org/project/ohlc-toolkit/)
[![Python](https://img.shields.io/pypi/pyversions/ohlc-toolkit.svg)](https://pypi.org/project/ohlc-toolkit/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0db6f73fe9bb4e8a8591055a6ea284f2)](https://app.codacy.com/gh/ff137/ohlc-toolkit/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/0db6f73fe9bb4e8a8591055a6ea284f2)](https://app.codacy.com/gh/ff137/ohlc-toolkit/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A flexible Python toolkit for working with OHLC (Open, High, Low, Close) market data.

## Installation

The project is available on [PyPI](https://pypi.org/project/ohlc-toolkit/):

```bash
pip install ohlc-toolkit
```

## Features

- Read OHLC data from CSV files into pandas DataFrames, with built-in data quality checks:

  ```py
    df = read_ohlc_csv(csv_file_path, timeframe="1d")
  ```

- Download bulk 1-minute Bitstamp BTCUSD candle data in one line (using data from [ff137/bitstamp-btcusd-minute-data](https://github.com/ff137/bitstamp-btcusd-minute-data)):

  ```py
    df_1min = BitstampDatasetDownloader().download_bitstamp_btcusd_minute_data(bulk=True)
  ```

- Transform 1-minute data into any timeframe you like:

  ```py
    df_5m = transform_ohlc(df_1min, timeframe=5)  # 5-minute candle length, updated every minute
    df_1h = transform_ohlc(df_1min, timeframe="1h", step_size_minutes=10)  # 1-hour data, updated every 10 minutes
    df_arb = transform_ohlc(df_1min, timeframe="1d3h7m")  # Arbitrary timeframes are supported
  ```

🚧 Coming soon™️:

- Calculate technical indicators
- Compute metrics for 'future' price-changes

All of the above features will enable you to generate extensive training data for machine learning models, whether for research or trading, to predict future price changes based on technical indicators.

## Examples

See the [examples](examples/README.md) directory for examples of how to use the toolkit.

Run the example script to see how the toolkit works:

```bash
# Clone the repository
git clone https://github.com/ff137/ohlc-toolkit.git
cd ohlc-toolkit

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install poetry
poetry install

# Run the example script
python examples/basic_usage.py
```

## Support

If you need any help or have any questions, please feel free to open an issue or contact me directly.

We hope this repo makes your life easier! If it does, please give us a star! ⭐
