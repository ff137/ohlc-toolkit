"""Tests for the pandas_ta.percent_return module."""

import unittest

import pandas as pd

from ohlc_toolkit.pandas_ta.percent_return import percent_return


class TestPercentReturn(unittest.TestCase):
    """Test the pandas_ta.percent_return module."""

    def setUp(self):
        """Set up the test environment."""
        self.close = pd.Series([100, 105, 110, 120, 130])

    def test_percent_return_default(self):
        """Test the default percent return."""
        result = percent_return(self.close)
        self.assertAlmostEqual(result.iloc[1], 0.05)
        self.assertTrue(result.isna().iloc[0])
        self.assertEqual(result.name, "PCTRET_1")
        self.assertEqual(result.category, "performance")

    def test_percent_return_length(self):
        """Test the percent return with a length."""
        result = percent_return(self.close, length=2)
        self.assertTrue(pd.isna(result.iloc[0]))
        self.assertTrue(pd.isna(result.iloc[1]))
        self.assertAlmostEqual(result.iloc[2], 0.10)

    def test_percent_return_cumulative(self):
        """Test the percent return with a cumulative."""
        result = percent_return(self.close, cumulative=True)
        self.assertAlmostEqual(result.iloc[0], 0.0)
        self.assertAlmostEqual(result.iloc[-1], 0.3)
        self.assertEqual(result.name, "CUMPCTRET_1")

    def test_percent_return_offset(self):
        """Test the percent return with an offset."""
        result = percent_return(self.close, offset=1)
        self.assertTrue(result.isna().iloc[0])
        self.assertTrue(result.isna().iloc[1])
        self.assertAlmostEqual(result.iloc[2], 0.05)

    def test_percent_return_fillna(self):
        """Test the percent return with a fillna."""
        result = percent_return(self.close, fillna=0)
        self.assertEqual(result.iloc[0], 0)

    def test_percent_return_short_series(self):
        """Test the percent return with a short series."""
        with self.assertRaises(ValueError):
            percent_return(pd.Series([1]), length=2)


if __name__ == "__main__":
    unittest.main()
