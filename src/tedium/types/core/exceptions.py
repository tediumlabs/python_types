"""Core exceptions for the tedium type system.

This module defines the exception hierarchy used throughout the type system.
All custom exceptions inherit from TypeSystemError to allow catching all
type-related errors with a single except clause.

Note on Type Usage:
    This module intentionally uses Python's built-in types (Dict, Any) rather than
    our custom types because:
    1. Exception context is an internal implementation detail
    2. We need to interoperate with Python's exception system
    3. Exception handling should be performant with minimal overhead
    4. Context needs to hold arbitrary Python values for debugging
    5. Avoiding circular dependencies (our types using exceptions that use our types)
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
