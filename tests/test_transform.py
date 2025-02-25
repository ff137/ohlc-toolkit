"""This module contains tests for the transform_ohlc function."""

import unittest

import pandas as pd

from ohlc_toolkit.csv_reader import read_ohlc_csv
from ohlc_toolkit.transform import transform_ohlc


class TestTransformOHLC(unittest.TestCase):
    """Test cases for the transform_ohlc function."""

    def setUp(self):
        """Set up the test case."""
        self.df = read_ohlc_csv("tests/test_data/real_world_data.csv", timeframe="1m")
        self.df_rows = self.df.shape[0]

    def test_transform_ohlc_3min_step_1(self):
        """Test transforming to 3-minute OHLC data with a step size of 1 minute."""
        transformed_df = transform_ohlc(self.df, timeframe="3m", step_size_minutes=1)

        # Check the shape of the transformed DataFrame
        self.assertEqual(transformed_df.shape[0], self.df_rows - 2)  # 2 rows dropped

        # Check the values of the first aggregated row
        high_first_3_rows = self.df.iloc[:3]["high"].max()
        open_first_3_rows = self.df.iloc[:3]["open"].iloc[0]
        low_first_3_rows = self.df.iloc[:3]["low"].min()
        close_first_3_rows = self.df.iloc[:3]["close"].iloc[-1]
        volume_first_3_rows = self.df.iloc[:3]["volume"].sum()

        self.assertEqual(transformed_df.iloc[0]["open"], open_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["high"], high_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["low"], low_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["close"], close_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["volume"], volume_first_3_rows)

        # Check the values of the second aggregated row (shifted by 1)
        high_next_3_rows = self.df.iloc[1:4]["high"].max()
        open_next_3_rows = self.df.iloc[1:4]["open"].iloc[0]
        low_next_3_rows = self.df.iloc[1:4]["low"].min()
        close_next_3_rows = self.df.iloc[1:4]["close"].iloc[-1]
        volume_next_3_rows = self.df.iloc[1:4]["volume"].sum()

        self.assertEqual(transformed_df.iloc[1]["open"], open_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["high"], high_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["low"], low_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["close"], close_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["volume"], volume_next_3_rows)

    def test_transform_ohlc_3min_step_3(self):
        """Test transforming to 3-minute OHLC data with a step size of 3 minutes."""
        transformed_df = transform_ohlc(self.df, timeframe="3m", step_size_minutes=3)

        # Check the shape of the transformed DataFrame
        self.assertEqual(
            transformed_df.shape[0], (self.df_rows - 2) // 3 + 1
        )  # 3-minute intervals

        # Check the values of the first aggregated row
        high_first_3_rows = self.df.iloc[:3]["high"].max()
        open_first_3_rows = self.df.iloc[:3]["open"].iloc[0]
        low_first_3_rows = self.df.iloc[:3]["low"].min()
        close_first_3_rows = self.df.iloc[:3]["close"].iloc[-1]
        volume_first_3_rows = self.df.iloc[:3]["volume"].sum()

        self.assertEqual(transformed_df.iloc[0]["open"], open_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["high"], high_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["low"], low_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["close"], close_first_3_rows)
        self.assertEqual(transformed_df.iloc[0]["volume"], volume_first_3_rows)

        # Check the values of the second aggregated row (shifted by 3)
        high_next_3_rows = self.df.iloc[3:6]["high"].max()
        open_next_3_rows = self.df.iloc[3:6]["open"].iloc[0]
        low_next_3_rows = self.df.iloc[3:6]["low"].min()
        close_next_3_rows = self.df.iloc[3:6]["close"].iloc[-1]
        volume_next_3_rows = self.df.iloc[3:6]["volume"].sum()

        self.assertEqual(transformed_df.iloc[1]["open"], open_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["high"], high_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["low"], low_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["close"], close_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["volume"], volume_next_3_rows)

    def test_transform_ohlc_6min_step_3(self):
        """Test transforming to 6-minute OHLC data with a step size of 3 minutes."""
        transformed_df = transform_ohlc(self.df, timeframe="6m", step_size_minutes=3)
        print(transformed_df)

        # Check the shape of the transformed DataFrame
        self.assertEqual(
            transformed_df.shape[0], (self.df_rows - 5) // 3 + 1
        )  # 6-minute intervals with 3 minute step size

        # Check the values of the first aggregated row
        high_first_6_rows = self.df.iloc[:6]["high"].max()
        open_first_6_rows = self.df.iloc[:6]["open"].iloc[0]
        low_first_6_rows = self.df.iloc[:6]["low"].min()
        close_first_6_rows = self.df.iloc[:6]["close"].iloc[-1]
        volume_first_6_rows = self.df.iloc[:6]["volume"].sum()

        self.assertEqual(transformed_df.iloc[0]["open"], open_first_6_rows)
        self.assertEqual(transformed_df.iloc[0]["high"], high_first_6_rows)
        self.assertEqual(transformed_df.iloc[0]["low"], low_first_6_rows)
        self.assertEqual(transformed_df.iloc[0]["close"], close_first_6_rows)
        self.assertEqual(transformed_df.iloc[0]["volume"], volume_first_6_rows)

        # Check the values of the second aggregated row (shifted by 3)
        high_next_3_rows = self.df.iloc[3:9]["high"].max()
        open_next_3_rows = self.df.iloc[3:9]["open"].iloc[0]
        low_next_3_rows = self.df.iloc[3:9]["low"].min()
        close_next_3_rows = self.df.iloc[3:9]["close"].iloc[-1]
        volume_next_3_rows = self.df.iloc[3:9]["volume"].sum()

        self.assertEqual(transformed_df.iloc[1]["open"], open_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["high"], high_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["low"], low_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["close"], close_next_3_rows)
        self.assertEqual(transformed_df.iloc[1]["volume"], volume_next_3_rows)

    def test_transform_with_non_datetime_index(self):
        """Test transforming a DataFrame with a non-datetime index."""
        # Reset the index to make it non-datetime
        print("self.df", self.df)
        df_non_datetime_index = self.df.reset_index(drop=True)
        print("df_non_datetime_index", df_non_datetime_index)

        # Transform the DataFrame
        transformed_df = transform_ohlc(
            df_non_datetime_index, timeframe="3m", step_size_minutes=3
        )

        # Check that the index of the transformed DataFrame is a DatetimeIndex
        # self.assertTrue(isinstance(transformed_df.index, pd.DatetimeIndex))

        # Check that the DataFrame is sorted by the datetime index
        self.assertTrue(transformed_df.index.is_monotonic_increasing)

    def test_transform_window_larger_than_data_with_step_size_1(self):
        """Test transforming a DataFrame with a window larger than the data (rolling case)."""
        # Transform the DataFrame
        with self.assertRaises(ValueError) as context:
            transform_ohlc(self.df, timeframe="2d", step_size_minutes=1)
        self.assertIn(
            "Please ensure your dataset is big enough "
            "for this timeframe: 2d (2880 minutes).",
            str(context.exception),
        )

    def test_transform_window_larger_than_data_with_step_size_2(self):
        """Test transforming a DataFrame with a window larger than the data (chunk case)."""
        # Transform the DataFrame
        with self.assertRaises(ValueError) as context:
            transform_ohlc(self.df, timeframe="2d", step_size_minutes=2)
        self.assertIn(
            "Please ensure your dataset is big enough "
            "for this timeframe: 2d (2880 minutes).",
            str(context.exception),
        )

    def test_transform_ohlc_with_string_timeframe(self):
        """Test transforming with a string timeframe."""
        transformed_df = transform_ohlc(self.df, timeframe="3m", step_size_minutes=1)
        self.assertIsInstance(transformed_df, pd.DataFrame)
        self.assertGreater(len(transformed_df), 0)

    def test_transform_ohlc_with_integer_timeframe(self):
        """Test transforming with an integer timeframe."""
        transformed_df = transform_ohlc(self.df, timeframe=3, step_size_minutes=1)
        self.assertIsInstance(transformed_df, pd.DataFrame)
        self.assertGreater(len(transformed_df), 0)

    def test_transform_ohlc_with_float_timeframe(self):
        """Test transforming with a float timeframe."""
        with self.assertRaises(ValueError):
            transform_ohlc(self.df, timeframe=3.5, step_size_minutes=1)

    def test_invalid_timeframe(self):
        """Test with an invalid timeframe."""
        with self.assertRaises(ValueError):
            transform_ohlc(self.df, timeframe="invalid", step_size_minutes=5)

    def test_non_integer_timeframe(self):
        """Test with a non-integer timeframe."""
        with self.assertRaises(NotImplementedError):
            transform_ohlc(self.df, timeframe="5s", step_size_minutes=5)


if __name__ == "__main__":
    unittest.main()
