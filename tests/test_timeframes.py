"""This module contains tests for the timeframes module."""

import unittest
from unittest.mock import Mock

from ohlc_toolkit.timeframes import (
    COMMON_TIMEFRAMES,
    format_timeframe,
    parse_timeframe,
    validate_timeframe,
    validate_timeframe_format,
)

arbitrary_timeframes = {
    "1h30m": (1 * 3600) + (30 * 60),  # 1 hour + 30 minutes
    "2d3h": (2 * 86400) + (3 * 3600),  # 2 days + 3 hours
    "1w2d": (1 * 604800) + (2 * 86400),  # 1 week + 2 days
    "3h45m": (3 * 3600) + (45 * 60),  # 3 hours + 45 minutes
    "2w1d4h30m": (2 * 604800) + (1 * 86400) + (4 * 3600) + (30 * 60),
}

reversed_arbitrary_timeframes = {
    seconds: timeframe for timeframe, seconds in arbitrary_timeframes.items()
}

common_timeframes_reversed = {
    seconds: timeframe for timeframe, seconds in COMMON_TIMEFRAMES.items()
}


class TestTimeframes(unittest.TestCase):
    """Test cases for the timeframes module."""

    def test_parse_common_timeframes(self):
        """Test parsing common timeframes."""
        for timeframe, expected_seconds in COMMON_TIMEFRAMES.items():
            with self.subTest(timeframe=timeframe):
                self.assertEqual(parse_timeframe(timeframe), expected_seconds)

    def test_parse_invalid_timeframes(self):
        """Test parsing invalid timeframe formats."""
        invalid_timeframes = [
            "",  # Empty string
            "1",  # Missing unit
            "m",  # Missing number
            "1x",  # Invalid unit
            "1h30",  # Missing unit for second part
            "1hm",  # Missing number for second part
            "h1",  # Wrong order
            "1.5h",  # Decimal not allowed
            "1h2",  # Missing unit at end
            "-1h",  # Negative not allowed
        ]

        for timeframe in invalid_timeframes:
            with self.subTest(timeframe=timeframe):
                with self.assertRaises(ValueError):
                    print(f"Testing {timeframe}")
                    parse_timeframe(timeframe)

    def test_format_timeframe(self):
        """Test formatting timeframes."""
        test_cases = common_timeframes_reversed | reversed_arbitrary_timeframes
        for seconds, expected_timeframe in test_cases.items():
            with self.subTest(seconds=seconds):
                self.assertEqual(format_timeframe(seconds), expected_timeframe)

    def test_validate_timeframe_format(self):
        """Test validating timeframe format."""
        valid_timeframes = ["1m", "2h", "3d", "4w", "1h30m", "2d3h", "1w2d"]
        invalid_timeframes = ["1x", "2h3", "3d4h5", "1h30", "2d3h4"]

        for timeframe in valid_timeframes:
            with self.subTest(timeframe=timeframe):
                print(f"Testing {timeframe}")
                self.assertTrue(validate_timeframe_format(timeframe))

        for timeframe in invalid_timeframes:
            with self.subTest(timeframe=timeframe):
                self.assertFalse(validate_timeframe_format(timeframe))

    def test_validate_timeframe(self):
        """Test validating timeframe."""
        # Test valid timeframe
        logger = Mock()

        time_step = 10
        user_timeframe = 100
        validate_timeframe(time_step, user_timeframe, logger)

        # Test invalid timeframe
        time_step = 10
        user_timeframe = 5
        with self.assertRaises(ValueError):
            validate_timeframe(time_step, user_timeframe, logger)

        # Test non-multiple timeframe
        time_step = 10
        user_timeframe = 25
        validate_timeframe(time_step, user_timeframe, logger)

        logger.warning.assert_called_with(
            "Provided timeframe (25s) is not a multiple "
            "of the inferred time step (10s). Data may be incomplete."
        )


if __name__ == "__main__":
    unittest.main()
