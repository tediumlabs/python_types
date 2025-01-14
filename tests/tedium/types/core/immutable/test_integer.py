"""Tests for the Integer immutable type implementation."""

from typing import Any, Dict, List, Set

import pytest

from tedium.types.core.exceptions import (
    IntegerValidationError,
    IntegerOverflowError,
)
from tedium.types.core.immutable.integer import Integer


def test_integer_basic_creation() -> None:
    """Test creating Integer with valid integer values."""
    # Test positive integer
    i = Integer(42)
    assert i.value == 42

    # Test zero
    i = Integer(0)
    assert i.value == 0

    # Test negative integer
    i = Integer(-42)
    assert i.value == -42


def test_integer_from_string() -> None:
    """Test creating Integer from valid string representations."""
    # Test positive integer string
    i = Integer.from_str("42")
    assert i.value == 42

    # Test negative integer string
    i = Integer.from_str("-42")
    assert i.value == -42

    # Test zero string
    i = Integer.from_str("0")
    assert i.value == 0

    # Test empty string
    with pytest.raises(IntegerValidationError) as exc_info:
        Integer.from_str("")
    assert "Empty string" in str(exc_info.value)

    # Test invalid string
    with pytest.raises(IntegerValidationError) as exc_info:
        Integer.from_str("not a number")
    assert "value" in str(exc_info.value)


def test_integer_from_float() -> None:
    """Test creating Integer from valid float values."""
    # Test whole number float
    i = Integer.from_float(42.0)
    assert i.value == 42

    # Test negative whole number float
    i = Integer.from_float(-42.0)
    assert i.value == -42

    # Test float with decimal part
    with pytest.raises(IntegerValidationError) as exc_info:
        Integer.from_float(42.5)
    assert "value" in str(exc_info.value)


def test_integer_validation_failures() -> None:
    """Test that invalid values raise appropriate exceptions."""
    # Test non-integer inputs using explicit Any typing
    invalid_inputs: List[Any] = ["42", 42.0, []]
    for invalid_input in invalid_inputs:
        with pytest.raises(IntegerValidationError):
            Integer(invalid_input)


def test_integer_comparison() -> None:
    """Test Integer comparison operations."""
    i1 = Integer(1)
    i2 = Integer(2)
    i3 = Integer(2)

    # Basic comparisons
    assert i1 < i2
    assert i2 > i1
    assert i1 <= i2
    assert i2 >= i1
    assert i2 == i3
    assert i1 != i2

    # Edge cases
    assert not (i2 < i3)
    assert not (i2 > i3)
    assert i2 <= i3
    assert i2 >= i3


def test_integer_comparison_with_other_types() -> None:
    """Test comparison operations with non-Integer types."""
    i = Integer(42)

    # Test equality with other types
    assert i != "42"
    assert i != 42
    assert i != 42.0

    # Test comparison operations with other types
    with pytest.raises(TypeError):
        i < "42"
    with pytest.raises(TypeError):
        i > "42"
    with pytest.raises(TypeError):
        i <= "42"
    with pytest.raises(TypeError):
        i >= "42"


def test_integer_string_representation() -> None:
    """Test string conversion methods."""
    i = Integer(42)

    # Test str()
    assert str(i) == "42"

    # Test repr()
    assert repr(i) == "Integer(42)"


def test_integer_hash() -> None:
    """Test that Integer instances can be used in sets and as dict keys."""
    # Test set operations
    s: Set[Integer] = {Integer(1), Integer(2), Integer(1)}
    assert len(s) == 2
    assert Integer(1) in s
    assert Integer(3) not in s

    # Test dict operations
    d: Dict[Integer, str] = {Integer(1): "one", Integer(2): "two"}
    assert d[Integer(1)] == "one"
    assert Integer(3) not in d


def test_integer_overflow() -> None:
    """Test that operations causing overflow raise appropriate exceptions."""
    max_int = Integer(2**63 - 1)  # Max 64-bit integer
    one = Integer(1)

    with pytest.raises(IntegerOverflowError) as exc_info:
        max_int + one
    assert "Cannot perform add between" in str(exc_info.value)


def test_integer_operation_errors() -> None:
    """Test that invalid operations raise TypeError."""
    i = Integer(42)
    other: Any = "not an integer"
    with pytest.raises(TypeError):
        i + other


def test_integer_validation() -> None:
    """Test Integer validation."""
    # Valid integer
    i = Integer(42)
    assert i.value == 42

    # None value
    with pytest.raises(IntegerValidationError) as exc_info:
        Integer(None)  # type: ignore
    assert "Value cannot be None" in str(exc_info.value)

    # Wrong type
    with pytest.raises(IntegerValidationError) as exc_info:
        Integer("42")  # type: ignore
    assert "Must be an integer, got str '42'" in str(exc_info.value)
