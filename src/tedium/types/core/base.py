"""Base type definitions for the tedium type system.

This module provides the foundational BaseType class that all other types
inherit from. It enforces immutability, validation, and provides core
functionality like string conversion, comparison operations, and JSON.
"""

from __future__ import annotations

import copy
import json
from functools import total_ordering
from typing import Any, Generic, TypeVar, Protocol, runtime_checkable
from abc import ABC, abstractmethod

from tedium.types.core.exceptions import (
    ValidationError,
    ConversionError,
    ImmutabilityError,
)

# Define return type for comparison operations
ComparisonReturn = Any  # This represents bool | type(NotImplemented)


@runtime_checkable
class Comparable(Protocol):
    """Protocol for types that support comparison operations."""
    def __lt__(self, other: Any) -> ComparisonReturn: ...
    def __gt__(self, other: Any) -> ComparisonReturn: ...
    def __le__(self, other: Any) -> ComparisonReturn: ...
    def __ge__(self, other: Any) -> ComparisonReturn: ...


T = TypeVar("T", bound=Comparable)


class BaseType(Generic[T], ABC):
    """Base class for all types in the tedium type system.

    This class follows Python's comparison protocol by returning NotImplemented
    for operations between incompatible types, allowing Python's type machinery
    to handle the TypeError generation.
    """

    _value: T

    def __init__(self, value: T) -> None:
        self.validate(value)
        object.__setattr__(self, "_value", value)

    @abstractmethod
    def validate(self, value: T) -> None:
        """Validate the value before storing it.

        Args:
            value: The value to validate

        Raises:
            ValidationError: If validation fails
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
            ImmutabilityError: If attempting to modify after initialization
        """
        # Allow setting _value during initialization
        if name == "_value" and not hasattr(self, "_value"):
            super().__setattr__(name, value)
            return

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

        Following Python's protocol, returns NotImplemented for incompatible types.

        Args:
            other: Value to compare against

        Returns:
            bool: True if values are equal
            NotImplemented: If types are incompatible
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value == other._value)

    def __lt__(self, other: Any) -> ComparisonReturn:
        """Compare if this value is less than another value.

        Following Python's protocol, returns NotImplemented for incompatible types.

        Args:
            other: Value to compare against

        Returns:
            bool | NotImplemented: True if this value is less than other, NotImplemented if incompatible
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value < other._value

    def __gt__(self, other: Any) -> bool:
        """Compare if this value is greater than another value."""
        if self.__class__ is BaseType:
            return NotImplemented
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value > other._value)

    def __le__(self, other: Any) -> bool:
        """Compare if this value is less than or equal to another value."""
        if self.__class__ is BaseType:
            return NotImplemented
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value <= other._value)

    def __ge__(self, other: Any) -> bool:
        """Compare if this value is greater than or equal to another value."""
        if self.__class__ is BaseType:
            return NotImplemented
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value >= other._value)

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


@total_ordering
class ComparableType(BaseType[T]):
    """Base class for types that support comparison operations."""

    def __lt__(self, other: Any) -> Any:
        """Compare if this value is less than another value."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value < other._value

    def __gt__(self, other: Any) -> bool:
        """Compare if this value is greater than another value."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value > other._value)

    def __le__(self, other: Any) -> bool:
        """Compare if this value is less than or equal to another value."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value <= other._value)

    def __ge__(self, other: Any) -> bool:
        """Compare if this value is greater than or equal to another value."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return bool(self._value >= other._value)
