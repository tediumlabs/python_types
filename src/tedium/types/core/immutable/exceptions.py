"""Exceptions for immutable integer types.

This module defines exceptions specific to immutable integer operations.
These inherit from the core type system exceptions to maintain the hierarchy
while keeping integer-specific error handling close to the implementation.
"""

from typing import Any

from tedium.types.core.exceptions import (
    ValidationError,
    ConversionError,
    OperationError,
)


class IntegerValidationError(ValidationError):
    """Raised when a value cannot be validated as an integer."""

    def __init__(self, value: Any, **context: Any) -> None:
        """Initialize with invalid integer value.

        Args:
            value: The invalid value
            **context: Additional validation context
        """
        message = f"Value '{value}' cannot be converted to an integer"
        super().__init__(message, value, **context)


class IntegerConversionError(ConversionError):
    """Raised when a value cannot be converted to an integer."""

    def __init__(self, value: Any, **context: Any) -> None:
        """Initialize with conversion details.

        Args:
            value: The value that couldn't be converted
            **context: Additional conversion context
        """
        message = f"Cannot convert '{value}' to integer"
        super().__init__(message, value, int, **context)


class IntegerOperationError(OperationError):
    """Raised when an integer operation cannot be performed."""

    def __init__(self, operation: str, left: Any, right: Any, **context: Any) -> None:
        """Initialize with operation details.

        Args:
            operation: The name of the failed operation
            left: The left operand
            right: The right operand
            **context: Additional operation context
        """
        message = f"Cannot perform {operation} between {left} and {right}"
        super().__init__(message, operation, left=left, right=right, **context)


class IntegerOverflowError(OperationError):
    """Raised when an integer operation would result in overflow."""

    def __init__(self, value: Any, operation: str) -> None:
        """Initialize the error with the value and operation that caused overflow.

        Args:
            value: The value that would cause overflow
            operation: The operation being performed (e.g. "addition")
        """
        message = f"Integer operation '{operation}' would overflow with value {value}"
        super().__init__(value=value, operation=operation, message=message)
