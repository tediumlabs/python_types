"""Tests for core type system exceptions."""

import pytest

from tedium.types.core.exceptions import (
    TypeSystemError,
    ValidationError,
    ConversionError,
    OperationError,
    ImmutabilityError,
)


def test_type_system_error() -> None:
    """Test base exception with context."""
    error = TypeSystemError("test error", key="value")
    assert str(error) == "test error"
    assert error.context == {"key": "value"}


def test_validation_error() -> None:
    """Test validation error with invalid value."""
    error = ValidationError("invalid value", value=123, min_value=0, max_value=100)
    assert str(error) == "invalid value"
    assert error.value == 123
    assert error.context == {"value": 123, "min_value": 0, "max_value": 100}


def test_conversion_error() -> None:
    """Test conversion error with target type."""
    error = ConversionError("cannot convert", value="abc", target_type=int)
    assert str(error) == "cannot convert"
    assert error.value == "abc"
    assert error.target_type == int
    assert error.context == {"value": "abc", "target_type": int}


def test_operation_error() -> None:
    """Test operation error with operation name."""
    error = OperationError("operation failed", operation="add")
    assert str(error) == "operation failed"
    assert error.operation == "add"
    assert error.context == {"operation": "add"}


def test_immutability_error() -> None:
    """Test immutability error with attribute."""
    error = ImmutabilityError("cannot modify", attribute="value")
    assert str(error) == "cannot modify"
    assert error.operation == "modify"
    assert error.attribute == "value"
    assert error.context == {"operation": "modify", "attribute": "value"}


def test_exception_hierarchy() -> None:
    """Test exception inheritance relationships."""
    # All exceptions inherit from TypeSystemError
    assert issubclass(ValidationError, TypeSystemError)
    assert issubclass(ConversionError, TypeSystemError)
    assert issubclass(OperationError, TypeSystemError)

    # ImmutabilityError inherits from OperationError
    assert issubclass(ImmutabilityError, OperationError)

    # Can catch all exceptions with TypeSystemError
    try:
        raise ImmutabilityError("test", attribute="value")
    except TypeSystemError as e:
        assert isinstance(e, ImmutabilityError)
