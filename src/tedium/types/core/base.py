"""Base type definitions for the tedium type system.

This module provides the foundational BaseType class that all other types
inherit from. It enforces immutability, validation, and provides core
functionality like string conversion, comparison operations, and JSON.
"""

from __future__ import annotations

import copy
import json
from functools import total_ordering
from typing import Any, Generic, TypeVar

from tedium.types.core.exceptions import (
    ValidationError,
    ConversionError,
    ImmutabilityError,
)


T = TypeVar("T")


@total_ordering
class BaseType(Generic[T]):
    """Base class for all types in the tedium type system.

    This class provides core functionality that all types inherit:
    - Immutability: Values cannot be changed after creation
    - Validation: Values are validated on creation
    - String conversion: Consistent string representation
    - Comparison operations: Types can be compared and sorted
    - JSON serialization: Types can be serialized to/from JSON
    - Copy support: Types can be copied safely

    Args:
        value: The value to wrap in this type

    Raises:
        ValidationError: If the value fails validation
        ConversionError: If the value cannot be converted to the required type
    """

    _value: T

    def __init__(self, value: T) -> None:
        """Initialize the type with a value.

        The value is validated and stored immutably.
        """
        self.validate(value)
        # Use object.__setattr__ to bypass immutability during init
        object.__setattr__(self, "_value", value)

    def validate(self, value: T) -> None:
        """Validate the value before storing it.

        This base implementation only ensures the value is not None.
        Subclasses should override this to add their own validation.

        Args:
            value: The value to validate

        Raises:
            ValidationError: If the value is None
        """
        if value is None:
            raise ValidationError("Value cannot be None", value=value)

    @property
    def value(self) -> T:
        """Get the wrapped value.

        The value is returned as-is without any conversion.

        Returns:
            The wrapped value
        """
        return self._value

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent attribute modification after initialization.

        Args:
            name: Attribute name
            value: New value

        Raises:
            ImmutabilityError: Always, as modification is not allowed
        """
        raise ImmutabilityError(
            f"Cannot modify {name} after initialization",
            attribute=name
        )

    def __str__(self) -> str:
        """Convert to string representation.

        Returns:
            String representation of the value
        """
        return str(self._value)

    def __repr__(self) -> str:
        """Get detailed string representation.

        Returns:
            Detailed string showing type and value
        """
        return f"{self.__class__.__name__}({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        """Check if this type equals another value.

        Args:
            other: Value to compare against

        Returns:
            True if the values are equal, NotImplemented if types don't match
        """
        if not isinstance(other, BaseType):
            return NotImplemented
        return bool(self._value == other._value)

    def __lt__(self, other: Any) -> bool:
        """Check if this type is less than another value.

        Args:
            other: Value to compare against

        Returns:
            True if this value is less than other, NotImplemented if no match
        """
        if not isinstance(other, BaseType):
            return NotImplemented
        return bool(self._value < other._value)

    def __hash__(self) -> int:
        """Get hash value for use in sets and as dict keys.

        Returns:
            Hash of the wrapped value
        """
        return hash(self._value)

    def to_json(self) -> str:
        """Convert the value to a JSON string.

        Returns:
            JSON string representation
        """
        return json.dumps(self._value)

    @classmethod
    def from_json(cls, json_str: str) -> BaseType[T]:
        """Create a new instance from a JSON string.

        Args:
            json_str: JSON string to parse

        Returns:
            New instance with the parsed value

        Raises:
            ConversionError: If the JSON string cannot be parsed
        """
        try:
            value = json.loads(json_str)
            return cls(value)
        except json.JSONDecodeError as e:
            raise ConversionError(
                "Invalid JSON string",
                value=json_str,
                target_type=cls,
                error=str(e)
            ) from e

    def __copy__(self) -> BaseType[T]:
        """Create a shallow copy.

        Returns:
            New instance with the same value
        """
        return self.__class__(self._value)

    def __deepcopy__(self, memo: dict[int, Any]) -> BaseType[T]:
        """Create a deep copy.

        Args:
            memo: Memo dictionary for deepcopy

        Returns:
            New instance with a deep copy of the value
        """
        return self.__class__(copy.deepcopy(self._value, memo))
