# Tedium Python Types

A strongly typed Python library providing immutable and mutable type wrappers with strict validation and clear error handling.

## Core Principles

### Type Strict
- Every operation must be type-safe and validated
- No implicit type conversions
- Full mypy strict mode compliance

### Self-Documenting
- Clear and intuitive APIs
- Explicit error messages
- Comprehensive type hints
- Always use named parameters for clarity and safety

### Fail Fast
- Invalid states are impossible to create
- Errors raised at creation time
- Clear error messages with context

## Development Cycle

Each type in the library follows a strict development cycle:

1. **Design & Documentation (Pre-Implementation)**
   - Document type requirements and constraints
   - Define validation rules and error cases
   - Create usage examples
   - Plan test cases

2. **Implementation**
   - Create type class with validation
   - Implement required operations
   - Add type hints and docstrings
   - Create type-specific exceptions

3. **Testing**
   - Write comprehensive unit tests
   - Test all validation rules
   - Verify error messages
   - Test edge cases

4. **Documentation**
   - Update README with new type
   - Add usage examples
   - Document exceptions
   - Verify documentation accuracy

5. **Review & Commit**
   - Run linting and type checks
   - Verify all tests pass
   - Review documentation
   - Commit changes

## When to Use Custom Types vs Python Types

This library provides custom type wrappers, but they're not meant to replace all uses of Python's built-in types. Here's when to use each:

### Use Custom Types When:
1. **Public Interfaces**: Parameters and return values of public methods
   ```python
   def set_port(port: Integer) -> None:  # Use custom type for validation
   ```

2. **Data Validation**: Values that need constraints or validation
   ```python
   port = Integer(8080, min_value=1, max_value=65535)
   ```

3. **Business Logic**: Domain objects and value types
   ```python
   age = Integer(25, min_value=0)
   name = String("Alice", min_length=1)
   ```

4. **Cross-Service Communication**: Data passing between services
   ```python
   response = api_service.send(data=String(json_data))
   ```

### Use Python Types When:
1. **Internal Implementation**: Local variables and private methods
   ```python
   def _process_items(self) -> None:
       count = 0  # Simple counter, use int
       for item in self._items:
           count += 1
   ```

2. **Standard Library Interop**: Working with Python's built-in functions
   ```python
   items = list(filter(lambda x: x > 0, numbers))  # Use list for stdlib
   ```

3. **Performance-Critical Code**: Tight loops or data structure internals
   ```python
   for i in range(1000000):  # Use int for performance
       total += values[i]
   ```

4. **Infrastructure Code**: Exception handling, logging, internal state
   ```python
   def __init__(self) -> None:
       self._cache: Dict[str, Any] = {}  # Internal cache, use dict
   ```

### Example: Mixing Types Appropriately
```python
class UserService:
    def __init__(self) -> None:
        # Use dict for internal cache
        self._cache: Dict[str, User] = {}
    
    def get_user(self, user_id: String) -> User:
        # Use str for stdlib interop
        cache_key = str(user_id)
        
        # Use custom types for business logic
        if user_id.length < Integer(1):
            raise ValidationError("Invalid user ID")
            
        # Use Python types for implementation
        return self._cache.get(cache_key, User.empty())
```

## Exception Hierarchy

The library uses a structured exception hierarchy with base exceptions that are extended for each type:

```
TypeSystemError
├── ValidationError
│   ├── IntegerValidationError
│   ├── StringValidationError
│   └── ...
├── ConversionError
│   ├── IntegerConversionError
│   ├── StringConversionError
│   └── ...
└── OperationError
    ├── IntegerOperationError
    │   └── IntegerOverflowError
    ├── StringOperationError
    └── ImmutabilityError
```

### Base Exceptions

#### TypeSystemError
Base exception for all type system errors. Provides context for debugging:
```python
try:
    # Some operation
except TypeSystemError as e:
    print(e)  # Clear error message
    print(e.context)  # Dict with error details
```

### ValidationError
Raised when a value fails validation:
```python
try:
    Integer(-1, min_value=0)
except ValidationError as e:
    print(e)  # "Value -1 is less than minimum 0"
    print(e.value)  # -1
    print(e.context)  # {"value": -1, "min_value": 0}
```

### ConversionError
Raised when type conversion fails:
```python
try:
    Integer.from_json("invalid")
except ConversionError as e:
    print(e)  # "Cannot convert 'invalid' to Integer"
    print(e.value)  # "invalid"
    print(e.target_type)  # Integer
```

### OperationError
Base class for operation-specific errors:
```python
try:
    string_type + 123  # Invalid operation
except OperationError as e:
    print(e)  # "Cannot add Integer to String"
    print(e.operation)  # "add"
```

### ImmutabilityError
Raised when attempting to modify immutable values:
```python
try:
    integer_type.value = 123  # Cannot modify
except ImmutabilityError as e:
    print(e)  # "Cannot modify value after initialization"
    print(e.attribute)  # "value"
```

### Type-Specific Exceptions

Each type extends the base exceptions to provide more specific error handling:

#### IntegerValidationError
```python
try:
    Integer(42.5)  # Must be a whole number
except IntegerValidationError as e:
    print(e)  # "Value 42.5 must be a whole number"
```

#### IntegerOverflowError
```python
try:
    Integer(2**63) + Integer(1)  # Exceeds bounds
except IntegerOverflowError as e:
    print(e)  # "Operation would exceed maximum value"
```

## Implementation Patterns

### Type Implementation
Each type follows these patterns:

1. **Base Class Extension**
   ```python
   class Integer(BaseType[int]):
       """An immutable integer type with validation."""
   ```

2. **Validation**
   ```python
   def _validate(self, value: Any) -> None:
       if not isinstance(value, (int, float, str)):
           raise IntegerValidationError(
               f"Expected int, float, or str, got {type(value)}"
           )
   ```

3. **Type-Specific Operations**
   ```python
   def __add__(self, other: Integer) -> Integer:
       if not isinstance(other, Integer):
           raise IntegerOperationError("Can only add Integer to Integer")
       result = self._value + other._value
       if not (-2**63 <= result <= 2**63 - 1):
           raise IntegerOverflowError(result)
       return Integer(result)
   ```

### Testing Patterns

Each type's tests should cover:

1. **Creation & Validation**
   ```python
   def test_integer_creation() -> None:
       """Test creating Integer with valid values."""
       assert Integer(42).value == 42
       assert Integer("42").value == 42
       assert Integer(42.0).value == 42
   ```

2. **Invalid Inputs**
   ```python
   def test_integer_validation() -> None:
       """Test that invalid values raise appropriate errors."""
       with pytest.raises(IntegerValidationError):
           Integer(42.5)  # Not a whole number
   ```

3. **Operations & Errors**
   ```python
   def test_integer_addition() -> None:
       """Test addition between Integers."""
       assert Integer(1) + Integer(2) == Integer(3)
       with pytest.raises(IntegerOperationError):
           Integer(1) + "2"  # Invalid operation
   ```

## Installation

```bash
pip install tedium-python-types
```

## Development

```bash
# Clone the repository
git clone https://github.com/tediumlabs/python-types.git
cd python-types

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run type checks
poetry run mypy src tests
```

## Usage Example

```python
from tedium.types.core import Integer, String

# Create types with validation
try:
    age = Integer(25, min_value=0, max_value=150)
    name = String("Alice", min_length=1)
except ValidationError as e:
    print(f"Validation failed: {e}")
    print(f"Context: {e.context}")

# Immutable by default
try:
    age.value = 26  # Raises ImmutabilityError
except ImmutabilityError as e:
    print(f"Cannot modify: {e}")

# Type-safe operations
try:
    result = age + "invalid"  # Raises OperationError
except OperationError as e:
    print(f"Invalid operation: {e}")
    print(f"Operation attempted: {e.operation}")
```

## License

MIT

## Design Principles

### Python Protocol Compliance
- Follow Python's comparison protocol
- Return NotImplemented for incompatible operations
- Let Python handle type error generation
- Enable proper type coercion when appropriate

Example:
```python
# Our types follow Python's protocol:
integer = Integer(42)
string = "not an integer"

# Returns NotImplemented, Python raises TypeError
result = integer < string  # Raises TypeError

# But allows valid comparisons
assert Integer(1) < Integer(2)
```

This approach:
- Makes our types behave like built-in Python types
- Enables proper type coercion and comparison chains
- Provides clear error messages through Python's machinery
- Maintains type safety while following conventions
