# Core Types

This package provides wrapper types around Python's built-in types that add type safety, validation, and consistent interfaces.

## Features

- **Type Safety**: Explicit type checking and no implicit conversions
- **Validation**: Values must meet type-specific criteria
- **Consistent Interface**: All types share common operations (comparison, hashing, JSON serialization)
- **Immutability/Mutability Choice**: Each type has both immutable and mutable variants

## Design Philosophy

These types serve as a foundation for building domain-specific types. They are intentionally thin wrappers around Python's built-in types, following Python's conventions while adding type safety and validation.

### Immutable Types
- Values cannot be changed after creation
- Prevent accidental modifications
- Thread-safe by default
- Good for domain modeling and data validation

### Mutable Types
- Support standard Python operators (`+=`, `-=`, etc.)
- Behave like built-in Python types
- Good for counters, accumulators, and state management
- Follow principle of least surprise

## Usage

```python
from tedium.types.core import Integer, MutableInteger

# Immutable usage
age = Integer(30)
# age += 1  # TypeError: can't modify immutable type
new_age = Integer(age.value + 1)  # Create new instance

# Mutable usage
counter = MutableInteger(0)
counter += 1  # Works just like a regular Python int

# Domain-specific types can extend either variant
class PositiveInteger(Integer):
    def validate(self, value: int) -> None:
        super().validate(value)
        if value <= 0:
            raise ValueError("Value must be positive")

class Counter(MutableInteger):
    def increment(self, by: int = 1) -> None:
        self += by
```

## Available Types

Each core type comes in both immutable and mutable variants:

### Immutable
- `Integer`: Wraps `int`
- `String`: Wraps `str`
- `Float`: Wraps `float`
- `Boolean`: Wraps `bool`
- `Date`: Wraps `datetime.date`
- `DateTime`: Wraps `datetime.datetime`
- `Decimal`: Wraps `decimal.Decimal`

### Mutable
- `MutableInteger`: Mutable `int` wrapper
- `MutableString`: Mutable `str` wrapper
- `MutableFloat`: Mutable `float` wrapper
- `MutableBoolean`: Mutable `bool` wrapper
- `MutableDate`: Mutable `datetime.date` wrapper
- `MutableDateTime`: Mutable `datetime.datetime` wrapper
- `MutableDecimal`: Mutable `decimal.Decimal` wrapper

Each type inherits from `BaseType[T]` where `T` is the wrapped Python type. 