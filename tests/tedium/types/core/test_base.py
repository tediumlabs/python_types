"""Tests for the BaseType class."""

import copy
from typing import Dict, Set

import pytest

from tedium.types.core.base import BaseType, ComparableType
from tedium.types.core.exceptions import (
    ValidationError,
    ImmutabilityError,
    ConversionError,
)


class StringType(BaseType[str]):
    """Simple string type for testing base functionality."""

    def validate(self, value: str) -> None:
        """Validate string values."""
        super().validate(value)
        if not isinstance(value, str):
            raise ValidationError("Must be a string", value=value)


class ComparableInt(ComparableType[int]):
    """Simple integer type for testing comparison operations."""

    def validate(self, value: int) -> None:
        """Validate integer values."""
        super().validate(value)
        if not isinstance(value, int):
            raise ValidationError("Must be an integer", value=value)


def test_base_functionality() -> None:
    """Test core functionality through MinimalType."""
    t = StringType("test")

    # Test immutability
    with pytest.raises(ImmutabilityError):
        t._value = "new"

    # Test string conversion
    assert str(t) == "test"
    assert repr(t) == "StringType('test')"

    # Test JSON
    json_str = t.to_json()
    recreated = StringType.from_json(json_str)
    assert recreated == t


def test_comparison_functionality() -> None:
    """Test comparison operations through ComparableInt."""
    t1 = ComparableInt(1)
    t2 = ComparableInt(2)

    # Test comparisons
    assert t1 < t2
    assert t2 > t1


def test_validation() -> None:
    """Test validation behavior."""
    # Valid string
    t = StringType("test")
    assert t.value == "test"

    # None value
    with pytest.raises(ValidationError) as exc_info:
        StringType(None)  # type: ignore
    assert "Value cannot be None" in str(exc_info.value)

    # Wrong type
    with pytest.raises(ValidationError) as exc_info:
        StringType(42)  # type: ignore
    assert "Must be a string" in str(exc_info.value)


def test_json_operations() -> None:
    """Test JSON serialization/deserialization."""
    original = StringType("test")

    # Serialization
    json_str = original.to_json()
    assert json_str == '"test"'

    # Deserialization
    recreated = StringType.from_json(json_str)
    assert recreated == original

    # Invalid JSON
    with pytest.raises(ConversionError) as exc_info:
        StringType.from_json("invalid")
    assert "Invalid JSON string" in str(exc_info.value)


def test_copy_operations() -> None:
    """Test copy behavior."""
    original = StringType("test")

    # Shallow copy
    shallow = copy.copy(original)
    assert shallow == original
    assert shallow is not original

    # Deep copy
    deep = copy.deepcopy(original)
    assert deep == original
    assert deep is not original


def test_comparison_edge_cases() -> None:
    """Test comparison operations with edge cases."""
    t1 = ComparableInt(1)
    t2 = ComparableInt(1)  # Same value
    t3 = StringType("1")  # Different type

    # Equal values
    assert not (t1 < t2)
    assert not (t1 > t2)
    assert t1 <= t2
    assert t1 >= t2

    # Different types should raise TypeError
    with pytest.raises(TypeError):
        t1 < t3
    with pytest.raises(TypeError):
        t1 > t3
    with pytest.raises(TypeError):
        t1 <= t3
    with pytest.raises(TypeError):
        t1 >= t3


def test_comparison_type_safety() -> None:
    """Test comparison operations maintain type safety."""
    t1 = ComparableInt(1)

    # Compare with non-BaseType values should raise TypeError
    with pytest.raises(TypeError):
        t1 < 2
    with pytest.raises(TypeError):
        t1 > 0
    with pytest.raises(TypeError):
        t1 <= "2"
    with pytest.raises(TypeError):
        t1 >= None


def test_hash_behavior() -> None:
    """Test hash behavior and collection operations."""
    t1 = ComparableInt(1)
    t2 = ComparableInt(1)  # Same value
    t3 = ComparableInt(2)  # Different value

    # Hash equality
    assert hash(t1) == hash(t2)
    assert hash(t1) != hash(t3)

    # Dict operations
    d: Dict[ComparableInt, str] = {t1: "one"}
    assert d[t2] == "one"  # Can retrieve with equal value
    assert t3 not in d     # Different value not found

    # Set operations
    s: Set[ComparableInt] = {t1, t2, t3}
    assert len(s) == 2     # t1 and t2 collapse to one entry
