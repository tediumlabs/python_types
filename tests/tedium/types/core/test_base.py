"""Tests for the base type implementation."""

import copy
import json
from typing import Dict, Set

import pytest

from tedium.types.core.base import BaseType
from tedium.types.core.exceptions import (
    ValidationError,
    ConversionError,
    ImmutabilityError,
)


def test_base_type_creation() -> None:
    """Test creating a base type with a valid value."""
    value = "test"
    base = BaseType(value)
    assert base.value == value


def test_base_type_none_value() -> None:
    """Test that None values are rejected."""
    with pytest.raises(ValidationError, match="Value cannot be None"):
        BaseType(None)


def test_base_type_immutability() -> None:
    """Test that values cannot be changed after creation."""
    base = BaseType("test")
    with pytest.raises(ImmutabilityError):
        base.value = "new value"


def test_base_type_str() -> None:
    """Test string conversion."""
    base = BaseType("test")
    assert str(base) == "test"


def test_base_type_repr() -> None:
    """Test detailed string representation."""
    base = BaseType("test")
    assert repr(base) == "BaseType('test')"


def test_base_type_equality() -> None:
    """Test equality comparison."""
    base1 = BaseType("test")
    base2 = BaseType("test")
    base3 = BaseType("other")

    assert base1 == base2
    assert base1 != base3
    assert base1 != "test"  # Different type


def test_base_type_ordering() -> None:
    """Test ordering operations."""
    base1 = BaseType(1)
    base2 = BaseType(2)
    base3 = BaseType(3)

    assert base1 < base2 < base3
    assert base3 > base2 > base1
    assert base1 <= base2 <= base3
    assert base3 >= base2 >= base1


def test_base_type_hash() -> None:
    """Test hash operation for use in sets and as dict keys."""
    base1: BaseType[str] = BaseType("test")
    base2: BaseType[str] = BaseType("test")

    # Same value should have same hash
    assert hash(base1) == hash(base2)

    # Can be used as dict key
    d: Dict[BaseType[str], str] = {base1: "value"}
    assert d[base2] == "value"

    # Can be used in sets
    s: Set[BaseType[str]] = {base1, base2}
    assert len(s) == 1


def test_base_type_json() -> None:
    """Test JSON serialization and deserialization."""
    original = BaseType("test")
    json_str = original.to_json()

    # JSON string should be valid
    parsed = json.loads(json_str)
    assert parsed == "test"

    # Can recreate from JSON
    recreated = BaseType.from_json(json_str)
    assert recreated == original

    # Invalid JSON raises ConversionError
    with pytest.raises(ConversionError):
        BaseType.from_json("invalid json")


def test_base_type_copy() -> None:
    """Test shallow and deep copy operations."""
    original: BaseType[list[int]] = BaseType([1, 2, 3])

    # Shallow copy
    shallow = copy.copy(original)
    assert shallow == original
    assert shallow is not original
    assert shallow._value is original._value

    # Deep copy
    deep = copy.deepcopy(original)
    assert deep == original
    assert deep is not original
    assert deep._value is not original._value
