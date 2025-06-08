"""Tests for the pandas_ta.utils module."""

import unittest

import pandas as pd

from ohlc_toolkit.pandas_ta import utils


class TestUtils(unittest.TestCase):
    """Test the pandas_ta.utils module."""

    def test_v_bool(self):
        """Test the v_bool function."""
        self.assertTrue(utils.v_bool(True, False))
        self.assertFalse(utils.v_bool(False, True))
        self.assertTrue(utils.v_bool("not_bool", True))
        self.assertFalse(utils.v_bool("not_bool", False))

    def test_v_int(self):
        """Test the v_int function."""
        self.assertEqual(utils.v_int(5, 1), 5)
        self.assertEqual(utils.v_int(0, 1), 1)
        self.assertEqual(utils.v_int(None, 2), 2)

    def test_v_offset(self):
        """Test the v_offset function."""
        self.assertEqual(utils.v_offset(3), 3)
        self.assertEqual(utils.v_offset(0), 0)
        self.assertEqual(utils.v_offset(None), 0)

    def test_v_lowerbound(self):
        """Test the v_lowerbound function."""
        self.assertEqual(utils.v_lowerbound(5, 0, 1), 5)
        self.assertEqual(utils.v_lowerbound(0, 0, 1, strict=True), 1)
        self.assertEqual(utils.v_lowerbound(0, 0, 1, strict=False), 0)
        self.assertEqual(utils.v_lowerbound(-1, 0, 1), 1)
        self.assertEqual(utils.v_lowerbound(5, 0, 1, complement=True), 1)

    def test_v_pos_default(self):
        """Test the v_pos_default function."""
        self.assertEqual(utils.v_pos_default(5, 1), 5)
        self.assertEqual(utils.v_pos_default(0, 1), 1)
        self.assertEqual(utils.v_pos_default(-1, 1), 1)

    def test_v_series(self):
        """Test the v_series function."""
        s = pd.Series([1, 2, 3])
        self.assertIsInstance(utils.v_series(s, 2), pd.Series)
        self.assertIsNone(utils.v_series(s, 5))
        self.assertIsNone(utils.v_series(None, 1))


if __name__ == "__main__":
    unittest.main()
