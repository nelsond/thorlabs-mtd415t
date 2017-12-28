"""
This module provides helper functions

---
Nelson Darkwah Oppong, December 2017
n@darkwahoppong.com
"""


def validate_is_float_or_int(value, name):
    """
    Validates that value is of type float or int.

    Args:
        value: Value that will be validated
        name (string): Human readable name of the value used for error messages

    Raises:
        ValueError: If the value is neither a float nor an int
    """
    if type(value) != int and type(value) != float:
        raise ValueError('{} must be an integer or float'.format(name))


def validate_is_in_range(value, min_val, max_val, name, unit=''):
    """
    Validates that a numeric value is in the given range.

    Args:
        value: Value that will be validated
        min_val (float or int): Minimum acceptable value
        max_val (float or int): Maximum acceptable value
        name (string): Human readable name of the value used for error messages
        unit (string, default is ''): Human readable unit of the value used for
        error messages

    Raises:
        ValueError: If the value is neither a float nor an int
    """

    if value < min_val:
        raise ValueError('{} must be >= {}{}.'.format(name, min_val, unit))

    if value > max_val:
        raise ValueError('{} must be <= {}{}.'.format(name, max_val, unit))
