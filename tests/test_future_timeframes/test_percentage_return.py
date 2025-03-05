"""Test the percentage return calculation."""

import unittest

import pandas as pd

from ohlc_toolkit.future_returns.percentage_return import calculate_percentage_return


class TestPercentageReturn(unittest.TestCase):
    """Test cases for the percentage return calculation."""

    def setUp(self):
        """Set up test data."""
        self.df = pd.DataFrame(
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

    def test_calculate_percentage_return(self):
        """Test the percentage return calculation."""
        close_prices = self.df["close"]
        timestep_size = 1  # 1 minute
        future_return_length = 2  # 2 minutes

        expected_returns = pd.Series(
            [
                None,
                None,
                (102220.0 / 102228.0) - 1,
                (102163.0 / 102215.0) - 1,
            ]
        )

        pct_return = calculate_percentage_return(
            close=close_prices,
            timestep_size=timestep_size,
            future_return_length=future_return_length,
        )

        pd.testing.assert_series_equal(pct_return, expected_returns, check_names=False)

    def test_calculate_percentage_return_with_fillna(self):
        """Test the percentage return calculation with fillna."""
        close_prices = self.df["close"]
        timestep_size = 1  # 1 minute
        future_return_length = 2  # 2 minutes

        expected_returns = pd.Series(
            [
                0.0,
                0.0,
                (102220.0 / 102228.0) - 1,
                (102163.0 / 102215.0) - 1,
            ]
        )

        pct_return = calculate_percentage_return(
            close=close_prices,
            timestep_size=timestep_size,
            future_return_length=future_return_length,
            fillna=0,
        )

        pd.testing.assert_series_equal(pct_return, expected_returns, check_names=False)

    def test_calculate_percentage_return_with_bfill(self):
        """Test the percentage return calculation with bfill."""
        close_prices = self.df["close"]
        timestep_size = 1  # 1 minute
        future_return_length = 2  # 2 minutes

        expected_returns = pd.Series(
            [
                None,
                None,
                (102220.0 / 102228.0) - 1,
                (102163.0 / 102215.0) - 1,
            ]
        )
        pct_return = calculate_percentage_return(
            close=close_prices,
            timestep_size=timestep_size,
            future_return_length=future_return_length,
            fill_method="bfill",  # Doesn't change first two NaNs
        )

        pd.testing.assert_series_equal(pct_return, expected_returns, check_names=False)


if __name__ == "__main__":
    unittest.main()
