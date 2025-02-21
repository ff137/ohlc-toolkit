"""This module contains functions for parsing and formatting timeframes."""

import re
from logging import Logger

# Predefined common timeframes for faster lookup
COMMON_TIMEFRAMES = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "8h": 28800,
    "12h": 43200,
    "1d": 86400,
    "2d": 172800,
    "3d": 259200,
    "4d": 345600,
    "1w": 604800,
    "2w": 1209600,
    "3w": 1814400,
    "4w": 2419200,
}

# Regex pattern to parse timeframe strings
TIMEFRAME_PATTERN = re.compile(r"(\d+)([wdhms])", re.IGNORECASE)
TIMEFRAME_FORMAT_PATTERN = re.compile(r"^(\d+[wdhms])+$", re.IGNORECASE)

# Unit conversion
TIME_UNITS = {
    "w": 604800,  # Weeks to seconds
    "d": 86400,  # Days to seconds
    "h": 3600,  # Hours to seconds
    "m": 60,  # Minutes to seconds
    "s": 1,  # Seconds to seconds
}


def parse_timeframe(timeframe: str) -> int:
    """Convert a timeframe string (e.g., '1h', '4h30m', '1w3d7h14m') into total seconds.

    Arguments:
        timeframe (str): Human-readable timeframe.

    Returns:
        int: Total number of seconds.

    Raises:
        ValueError: If the format is invalid.
    """
    if not validate_timeframe_format(timeframe):
        raise ValueError(f"Invalid timeframe format: {timeframe}")

    matches = TIMEFRAME_PATTERN.findall(timeframe)
    total_seconds = sum(
        int(amount) * TIME_UNITS[unit.lower()] for amount, unit in matches
    )
    return total_seconds


def format_timeframe(seconds: int) -> str:
    """Convert a total number of seconds into a human-readable timeframe string.

    Arguments:
        seconds (int): Total number of seconds.

    Returns:
        str: Human-readable timeframe string (e.g., '1h', '4h30m').
    """
    if seconds in COMMON_TIMEFRAMES.values():
        # Return predefined common timeframes if found
        return {v: k for k, v in COMMON_TIMEFRAMES.items()}[seconds]

    units = [("w", 604800), ("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    parts = []

    for unit, unit_seconds in units:
        value, seconds = divmod(seconds, unit_seconds)
        if value > 0:
            parts.append(f"{value}{unit}")

    return "".join(parts)


def validate_timeframe_format(timeframe: str) -> bool:
    """Validate whether a given timeframe string follows the expected format.

    Arguments:
        timeframe (str): Timeframe string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(TIMEFRAME_FORMAT_PATTERN.fullmatch(timeframe))


def validate_timeframe(time_step: int, user_timeframe: int, logger: Logger):
    """Ensure that the timeframe is valid given the time step."""
    if user_timeframe < time_step:
        raise ValueError(
            f"Provided timeframe ({user_timeframe}s) cannot be smaller "
            f"than inferred time step ({time_step}s)."
        )

    if user_timeframe % time_step != 0:
        logger.warning(
            f"Provided timeframe ({user_timeframe}s) is not a multiple "
            f"of the inferred time step ({time_step}s). Data may be incomplete."
        )
