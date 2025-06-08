"""Test cases for the log configuration module."""

import importlib
import os
import unittest
from unittest.mock import patch

from loguru import logger

from ohlc_toolkit.config import logging
from ohlc_toolkit.config.logging import _get_log_file_path, get_logger


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
        actual_path = _get_log_file_path("ohlc_toolkit")
        self.assertEqual(expected_path, actual_path)

    @patch("sys.stdout.write")
    def test_serialization_format(self, mock_stdout):
        """Test that logs are serialized correctly."""
        with patch.dict(os.environ, {"ENABLE_SERIALIZE_LOGS": "TRUE"}):
            importlib.reload(logging)  # Reload the module to apply the env var
            test_logger = logging.get_logger("ohlc_toolkit.test_module2")
            test_logger.bind(body="extra info").info("Test message")

            # Check that the serialized log is written to stdout
            self.assertTrue(mock_stdout.called)
            serialized_output = mock_stdout.call_args[0][0]
            self.assertIn('"message":"Test message | extra info"', serialized_output)
            self.assertIn('"levelname":"INFO"', serialized_output)

    @patch("sys.stdout.write")
    def test_serialization_format_with_exception(self, mock_stdout):
        """Test that logs with exceptions are serialized correctly."""
        with patch.dict(os.environ, {"ENABLE_SERIALIZE_LOGS": "TRUE"}):
            importlib.reload(logging)  # Reload the module to apply the env var
            test_logger = logging.get_logger("ohlc_toolkit.test_module2")

            try:
                raise ValueError("An error occurred")
            except ValueError:
                test_logger.bind(body="extra info").exception("Test message")

            # Check that the serialized log is written to stdout
            self.assertTrue(mock_stdout.called)
            serialized_output = mock_stdout.call_args[0][0]
            self.assertIn('"message":"Test message | extra info"', serialized_output)
            self.assertIn('"levelname":"ERROR"', serialized_output)
            self.assertIn('"type":"ValueError"', serialized_output)
            self.assertIn('"value":"An error occurred"', serialized_output)

    @patch(
        "os.path.join",
        return_value="/fake/path/to/logs/ohlc_toolkit/{time:YYYY-MM-DD}.log",
    )
    @patch("loguru._logger.Logger.add")
    def test_enable_file_logging(self, mock_add, _):
        """Test that file logging is enabled and configured correctly."""
        with patch.dict(os.environ, {"ENABLE_FILE_LOGGING": "TRUE"}):
            importlib.reload(logging)  # Reload the module to apply the env var
            test_logger = logging.get_logger("ohlc_toolkit.test_module")
            test_logger.info("Test message")
            mock_add.assert_any_call(
                "/fake/path/to/logs/ohlc_toolkit/{time:YYYY-MM-DD}.log",
                rotation="00:00",
                retention="7 days",
                enqueue=True,
                level=logging.FILE_LOG_LEVEL,
                diagnose=True,
                format=unittest.mock.ANY,
                serialize=unittest.mock.ANY,
            )

    def side_effect_for_add(*args, **_):
        """Raise PermissionError on the second call."""
        if hasattr(logging, "call_count"):
            logging.call_count += 1
        else:
            logging.call_count = 1  # type: ignore

        if logging.call_count == 2:  # type: ignore # noqa: PLR2004
            raise PermissionError("Mocked permission error")

    @patch("loguru._logger.Logger.add", side_effect=side_effect_for_add)
    @patch("loguru._logger.Logger.warning")
    def test_file_logging_permission_error(self, mock_warning, _):
        """Test that a warning is logged when PermissionError occurs."""
        with patch.dict(os.environ, {"ENABLE_FILE_LOGGING": "TRUE"}):
            importlib.reload(logging)  # Reload the module to apply the env var
            test_logger = logging.get_logger("ohlc_toolkit.test_module")

            # Trigger a log to ensure the logger is initialized
            test_logger.info("Trigger log")

            # Check that the warning about the PermissionError was logged
            mock_warning.assert_called_with(
                "Permission error caught when trying to create log file. "
                "Continuing without file logging for `{}` in `{}`",
                "ohlc_toolkit.test_module",
                "ohlc_toolkit",
            )


if __name__ == "__main__":
    unittest.main()
