# Examples

This `examples` directory contains scripts that demonstrate
how to use the toolkit for processing OHLC data.

## Prerequisites

First, clone the `ohlc-toolkit` repository:

```bash
git clone https://github.com/ff137/ohlc-toolkit.git
```

Set up a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate

pip install poetry
poetry install
```

### Getting a Sample Dataset

Before running the examples, you need a sample dataset to work with.

On a [separate repo](https://github.com/ff137/bitstamp-btcusd-minute-data), we host up-to-date BTC/USD 1-minute data from Bitstamp,
which can be found at the following link:

<https://github.com/ff137/bitstamp-btcusd-minute-data/blob/main/data/updates/btcusd_bitstamp_1min_latest.csv>

Inspect the above link to verify that you're happy downloading the data.

Feel free to click the download button, or use the following command:

```bash
cd ohlc-toolkit  # Move to the project
mkdir -p data  # Create a data directory

curl -L -o data/btcusd_bitstamp_1min_latest.csv https://github.com/ff137/bitstamp-btcusd-minute-data/raw/main/data/updates/btcusd_bitstamp_1min_latest.csv
```

We recommend the above data because it is real, recent, and has passed
data quality checks. You're of course welcome to use your own dataset instead.

## Running the Example

Once you have downloaded the data, you can run the `basic_usage.py` script
to see how the `ohlc-toolkit` processes the data.

### Instructions

Verify that the `btcusd_bitstamp_1min_latest.csv` file is located in the `ohlc-toolkit/data` directory.

Then, run the following command in your terminal:

```bash
python examples/basic_usage.py
```

### What the Script Does

The [basic_usage.py](basic_usage.py) script performs the following actions:

- Imports the `ohlc_toolkit` module.
- Reads the OHLC data from the CSV file using the `read_ohlc_csv` function.

That's it for now! More features will be added soon.
