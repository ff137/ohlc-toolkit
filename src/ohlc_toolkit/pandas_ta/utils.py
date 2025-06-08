"""Utility functions from pandas-ta."""

from functools import partial
from typing import Any

from numpy import floating as np_floating
from numpy import integer as np_integer
from pandas import Series

IntFloat = int | float


def v_bool(var: bool | Any, default: bool = True) -> bool:
    """Validate the var is a bool.

    Returns the default if var is not a bool.
    """
    if isinstance(var, bool):
        return var
    return default


def v_int(var: int, default: int, ne: int | None = 0) -> int:
    """Validate the var is not equal to the ne value.

    Returns the default if var is not equal to the ne value.
    """
    if isinstance(var, int) and int(var) != int(ne):
        return int(var)
    if isinstance(var, np_integer) and var.item() != int(ne):
        return var.item()
    return int(default)


def v_offset(var: int) -> int:
    """Defaults to 0."""
    return partial(v_int, default=0, ne=0)(var=var)


def v_lowerbound(
    var: IntFloat,
    bound: IntFloat = 0,
    default: IntFloat = 0,
    strict: bool = True,
    complement: bool = False,
) -> IntFloat:
    """Validate the var is greater than bound.

    Returns the default if var is not greater than bound. If strict is False,
    the var is also allowed to be equal to the bound.

    Args:
        var (IntFloat): The variable to validate.
        bound (IntFloat): The bound to validate against.
        default (IntFloat): The default value to return if the var is not greater (or equal) than bound.
        strict (bool): Whether to use strict comparison.
        complement (bool): Whether to complement the validation.

    Returns:
        IntFloat: The validated var.

    """
    var_type = None
    if isinstance(var, float | np_floating):
        var_type = float
    if isinstance(var, int | np_integer):
        var_type = int

    if var_type is None:
        return default

    valid = False
    if strict:
        valid = var_type(var) > var_type(bound)
    else:
        valid = var_type(var) >= var_type(bound)

    if complement:
        valid = not valid

    if valid:
        return var_type(var)
    return default


def v_pos_default(
    var: IntFloat, default: IntFloat = 0, strict: bool = True, complement: bool = False
) -> IntFloat:
    """Validate the var is greater than 0.

    Returns the default if var is not greater than 0.
    """
    return partial(v_lowerbound, bound=0)(
        var=var, default=default, strict=strict, complement=complement
    )


def v_series(series: Series, length: IntFloat | None = 0) -> Series | None:
    """Validate the series and length required for the indicator.

    Returns None if the Pandas Series does not meet the minimum length required for the indicator.

    Args:
        series (Series): The series to validate.
        length (IntFloat | None): The minimum length required for the indicator.

    Returns:
        Series | None: The validated series or None if the series does not meet the minimum length.

    """
    if series is not None and isinstance(series, Series):
        if series.size >= v_pos_default(length, 0):
            return series
    return None
