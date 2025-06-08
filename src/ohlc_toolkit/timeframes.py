"""Functions for parsing and formatting timeframes."""

import re
from logging import Logger

MINUTE_SECONDS = 60
HOUR_MINUTES = 60
DAY_HOURS = 24
WEEK_DAYS = 7

HOUR_SECONDS = MINUTE_SECONDS * HOUR_MINUTES
DAY_SECONDS = HOUR_SECONDS * DAY_HOURS
WEEK_SECONDS = DAY_SECONDS * WEEK_DAYS

# Predefined common timeframes for faster lookup
COMMON_TIMEFRAMES = {
    "1m": MINUTE_SECONDS,
    "3m": MINUTE_SECONDS * 3,
    "5m": MINUTE_SECONDS * 5,
    "15m": MINUTE_SECONDS * 15,
    "30m": MINUTE_SECONDS * 30,
    "1h": HOUR_SECONDS,
    "2h": HOUR_SECONDS * 2,
    "4h": HOUR_SECONDS * 4,
    "6h": HOUR_SECONDS * 6,
    "8h": HOUR_SECONDS * 8,
    "12h": HOUR_SECONDS * 12,
    "1d": DAY_SECONDS,
    "2d": DAY_SECONDS * 2,
    "3d": DAY_SECONDS * 3,
    "4d": DAY_SECONDS * 4,
    "1w": WEEK_SECONDS,
    "2w": WEEK_SECONDS * 2,
    "3w": WEEK_SECONDS * 3,
    "4w": WEEK_SECONDS * 4,
}

# Regex pattern to parse timeframe strings
TIMEFRAME_PATTERN = re.compile(r"(\d+)([wdhms])", re.IGNORECASE)
TIMEFRAME_FORMAT_PATTERN = re.compile(r"^(\d+[wdhms])+$", re.IGNORECASE)

# Unit conversion
TIME_UNITS = {
    "w": WEEK_SECONDS,
    "d": DAY_SECONDS,
    "h": HOUR_SECONDS,
    "m": MINUTE_SECONDS,
    "s": 1,
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


def format_timeframe(seconds: int | str) -> str:
    """Convert a total number of seconds into a human-readable timeframe string.

    Arguments:
        seconds (int | str): Total number of seconds.
            If a string is provided, it is assumed to be a valid timeframe string.

    Returns:
        str: Human-readable timeframe string (e.g., '1h', '4h30m').

    """
    if isinstance(seconds, str):
        return seconds

    if seconds in COMMON_TIMEFRAMES.values():
        # Return predefined common timeframes if found
        return {v: k for k, v in COMMON_TIMEFRAMES.items()}[seconds]

    units = [
        ("w", WEEK_SECONDS),
        ("d", DAY_SECONDS),
        ("h", HOUR_SECONDS),
        ("m", MINUTE_SECONDS),
        ("s", 1),
    ]
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
            f"Requested timeframe ({user_timeframe}s) should not be smaller "
            f"than time step ({time_step}s)."
        )

    if user_timeframe % time_step != 0:
        logger.warning(
            f"Note: Requested timeframe ({user_timeframe}s) is not a multiple "
            f"of the time step ({time_step}s); values may not be suitable."
        )
