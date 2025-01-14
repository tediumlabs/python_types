"""Core exceptions for the tedium type system.

This module defines the exception hierarchy used throughout the type system.
All custom exceptions inherit from TypeSystemError to allow catching all
type-related errors with a single except clause.
"""

from typing import Any, Dict


class TypeSystemError(Exception):
    """Base exception for all type system errors."""

    context: Dict[str, Any]

    def __init__(self, message: str, **context: Any) -> None:
        """Initialize with message and optional context.

        Args:
            message: The error message
            **context: Additional context about the error
        """
        super().__init__(message)
        self.context = context


class ValidationError(TypeSystemError):
    """Raised when a value fails validation."""

    value: Any

    def __init__(self, message: str, value: Any, **context: Any) -> None:
        """Initialize with invalid value information.

        Args:
            message: The validation error message
            value: The invalid value
            **context: Additional validation context
        """
        super().__init__(message, value=value, **context)
        self.value = value


class ConversionError(TypeSystemError):
    """Raised when a value cannot be converted to the target type."""

    value: Any
    target_type: type

    def __init__(self, message: str, value: Any, target_type: type, **context: Any) -> None:
        """Initialize with conversion details.

        Args:
            message: The conversion error message
            value: The value that couldn't be converted
            target_type: The type we tried to convert to
            **context: Additional conversion context
        """
        super().__init__(message, value=value, target_type=target_type, **context)
        self.value = value
        self.target_type = target_type


class OperationError(TypeSystemError):
    """Raised when an operation cannot be performed."""

    operation: str

    def __init__(self, message: str, operation: str, **context: Any) -> None:
        """Initialize with operation details.

        Args:
            message: The operation error message
            operation: The name of the failed operation
            **context: Additional operation context
        """
        super().__init__(message, operation=operation, **context)
        self.operation = operation


class ImmutabilityError(OperationError):
    """Raised when attempting to modify an immutable value."""

    attribute: str

    def __init__(self, message: str, attribute: str, **context: Any) -> None:
        """Initialize with immutability violation details.

        Args:
            message: The immutability error message
            attribute: The attribute that was attempted to be modified
            **context: Additional context
        """
        super().__init__(message, operation="modify", attribute=attribute, **context)
        self.attribute = attribute


# Integer-specific exceptions
class IntegerValidationError(ValidationError):
    """Raised when a value cannot be validated as an integer."""

    def __init__(self, value: Any, **context: Any) -> None:
        """Initialize with invalid integer value.

        Args:
            value: The invalid value
            **context: Additional validation context
        """
        message = f"Invalid value: {value}"
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
        """Initialize with operation details."""
        message = f"Cannot perform {operation} between {left} and {right}"
        super().__init__(operation=operation, left=left, right=right, message=message)


class IntegerOverflowError(IntegerOperationError):
    """Raised when an integer operation would result in overflow."""

    def __init__(self, operation: str, result: Any, **context: Any) -> None:
        """Initialize with overflow details."""
        message = f"Operation {operation} would overflow: {result}"
        super().__init__(
            operation=operation,
            left=context.pop('left'),
            right=context.pop('right'),
            message=message
        )
