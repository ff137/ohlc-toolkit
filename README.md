# OHLC Toolkit

[![PyPI](https://img.shields.io/pypi/v/ohlc-toolkit)](https://pypi.org/project/ohlc-toolkit/)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/MIT)

A flexible Python toolkit for working with OHLC (Open, High, Low, Close) market data.

## Features

- Read OHLC data from CSV files, with built-in data quality checks
- Process high resolution data (e.g. 1-minute interval data) into any greater time frame
  (e.g. turn 1-minute data into 15-minute, 1-hour, 4-hour, 1-day, etc.)

Coming soon™️:

- Calculate technical indicators
- Compute metrics for 'future' price-changes

Essentially, the above features will provide you with the capability to generate input and output data for
training a machine learning model to predict future price-changes based on technical indicators.

## Examples

See the [examples](examples/README.md) directory for examples of how to use the toolkit.

## Installation

The project is available on [PyPI](https://pypi.org/project/ohlc-toolkit/):

```bash
pip install ohlc-toolkit
```

## Support

If you need any help or have any questions, please feel free to open an issue or contact me directly.

We hope this repo makes your life easier! If it does, please give us a star! ⭐
