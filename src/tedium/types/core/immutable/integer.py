"""Integer type implementation.

This module provides an immutable Integer type that wraps Python's int type,
adding validation and type safety.
"""

from typing import Any

from ..base import BaseType
from tedium.types.core.exceptions import (
    IntegerValidationError,
    IntegerOverflowError,
)


class Integer(BaseType[int]):
    """An immutable integer type.

    This type wraps Python integers and ensures type safety and immutability.
    Following Python's comparison protocol, operations between incompatible
    types return NotImplemented rather than raising exceptions.
    """

    def __init__(self, value: int) -> None:
        """Initialize an Integer with a value.

        Args:
            value: An integer value.

        Raises:
            IntegerValidationError: If the value is not an integer
        """
        if value is None:
            raise IntegerValidationError("Value cannot be None")
        if not isinstance(value, int):
            raise IntegerValidationError(f"Must be an integer, got {type(value).__name__} '{value}'")

        super().__init__(value)

    @classmethod
    def from_str(cls, value: str) -> "Integer":
        """Create an Integer from a string.

        Args:
            value: String representation of an integer

        Returns:
            Integer instance

        Raises:
            IntegerValidationError: If the string is empty or invalid
        """
        if not value.strip():
            raise IntegerValidationError("Empty string")
        try:
            return cls(int(value))
        except ValueError as e:
            raise IntegerValidationError(value) from e

    @classmethod
    def from_float(cls, value: float) -> "Integer":
        """Create an Integer from a float.

        Args:
            value: Float that represents a whole number

        Returns:
            Integer instance

        Raises:
            IntegerValidationError: If the float is not a whole number
        """
        if not value.is_integer():
            raise IntegerValidationError(value)
        return cls(int(value))

    @property
    def value(self) -> int:
        """Get the underlying integer value.

        Returns:
            int: The wrapped integer value.
        """
        return self._value

    def __add__(self, other: Any) -> "Integer":
        """Add this Integer to another value.

        Args:
            other: The value to add

        Returns:
            Integer: A new Integer with the sum
            NotImplemented: If other is not an Integer

        Raises:
            IntegerOverflowError: If the result would overflow
        """
        if not isinstance(other, Integer):
            return NotImplemented

        try:
            result = self._value + other._value
            if result > 2**63 - 1 or result < -(2**63):
                raise IntegerOverflowError("add", result, left=self, right=other)
            return Integer(result)
        except OverflowError:
            raise IntegerOverflowError("add", f"{self._value} + {other._value}", left=self, right=other)

    def __eq__(self, other: Any) -> bool:
        """Compare this Integer with another value for equality.

        Args:
            other: Value to compare against

        Returns:
            bool: True if the values are equal, False otherwise
        """
        if not isinstance(other, Integer):
            return False
        return self._value == other._value

    def __lt__(self, other: Any) -> Any:
        """Compare if this Integer is less than another value."""
        if not isinstance(other, Integer):
            return NotImplemented
        return self._value < other._value

    def __gt__(self, other: Any) -> Any:
        """Compare if this Integer is greater than another value."""
        if not isinstance(other, Integer):
            return NotImplemented
        return self._value > other._value

    def __le__(self, other: Any) -> Any:
        """Compare if this Integer is less than or equal to another value."""
        if not isinstance(other, Integer):
            return NotImplemented
        return self._value <= other._value

    def __ge__(self, other: Any) -> Any:
        """Compare if this Integer is greater than or equal to another value."""
        if not isinstance(other, Integer):
            return NotImplemented
        return self._value >= other._value

    def __hash__(self) -> int:
        """Get hash value for use in sets and as dict keys.

        Returns:
            int: Hash of the wrapped value
        """
        return hash(self._value)

    def __str__(self) -> str:
        """Get string representation of the integer value.

        Returns:
            str: The string representation of the wrapped integer.
        """
        return str(self._value)

    def __repr__(self) -> str:
        """Get detailed string representation.

        Returns:
            str: A string in the format 'Integer(value)'.
        """
        return f"Integer({self._value})"

    def validate(self, value: int) -> None:
        """Validate integer values."""
        if value is None:
            raise IntegerValidationError("Value cannot be None")
        if not isinstance(value, int):
            raise IntegerValidationError(f"Must be an integer, got {type(value).__name__} '{value}'")
