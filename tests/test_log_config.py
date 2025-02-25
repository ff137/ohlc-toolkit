"""Test cases for the log configuration module."""

import importlib
import os
import unittest
from unittest.mock import patch

from loguru import logger

import ohlc_toolkit.config.log_config as log_config
from ohlc_toolkit.config.log_config import get_log_file_path, get_logger


class TestLogConfig(unittest.TestCase):
    """Test cases for the log configuration module."""

    def test_get_logger_instance(self):
        """Test that get_logger returns a logger instance."""
        test_logger = get_logger("ohlc_toolkit.test_module")
        self.assertIsInstance(test_logger, logger.__class__)

    def test_log_file_path(self):
        """Test that the log file path is correctly generated."""
        expected_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "logs/ohlc_toolkit/{time:YYYY-MM-DD}.log",
        )
        actual_path = get_log_file_path("ohlc_toolkit")
        self.assertEqual(expected_path, actual_path)

    @patch("sys.stdout.write")
    def test_serialization_format(self, mock_stdout):
        """Test that logs are serialized correctly."""
        with patch.dict(os.environ, {"ENABLE_SERIALIZE_LOGS": "TRUE"}):
            importlib.reload(log_config)  # Reload the module to apply the env var
            test_logger = log_config.get_logger("ohlc_toolkit.test_module2")
            test_logger.bind(body="extra info").info("Test message")

            # Check that the serialized log is written to stdout
            self.assertTrue(mock_stdout.called)
            serialized_output = mock_stdout.call_args[0][0]
            self.assertIn('"message":"Test message | extra info"', serialized_output)
            self.assertIn('"levelname":"INFO"', serialized_output)

    @patch(
        "os.path.join",
        return_value="/fake/path/to/logs/ohlc_toolkit/{time:YYYY-MM-DD}.log",
    )
    @patch("loguru._logger.Logger.add")
    def test_enable_file_logging(self, mock_add, _):
        """Test that file logging is enabled and configured correctly."""
        with patch.dict(os.environ, {"ENABLE_FILE_LOGGING": "TRUE"}):
            importlib.reload(log_config)  # Reload the module to apply the env var
            test_logger = log_config.get_logger("ohlc_toolkit.test_module")
            test_logger.info("Test message")
            mock_add.assert_any_call(
                "/fake/path/to/logs/ohlc_toolkit/{time:YYYY-MM-DD}.log",
                rotation="00:00",
                retention="7 days",
                enqueue=True,
                level=log_config.FILE_LOG_LEVEL,
                diagnose=True,
                format=unittest.mock.ANY,
                serialize=unittest.mock.ANY,
            )


if __name__ == "__main__":
    unittest.main()
