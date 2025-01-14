# Tedium Labs Python Types

A Python library for building strongly-typed domain models with runtime validation and immutability.

## Features

- Core value types with runtime validation and immutability
- Composable type system for building complex domain models
- Type-safe collections and containers
- Serialization support for JSON and other formats
- Comprehensive test coverage and static type checking

## Installation

```bash
pip install tedium-python-types
```

## Quick Start

```python
from tedium.types.core import StringType, IntegerType
from tedium.types.collections import TypedList
from tedium.types.domain import DomainType

# Define a simple value type
class PortNumber(IntegerType):
    def validate(self, value: int) -> None:
        super().validate(value)
        if not 0 <= value <= 65535:
            raise ValueError("Port number must be between 0 and 65535")

# Use in your domain models
class ServerConfig(DomainType):
    def __init__(self, host: StringType, port: PortNumber):
        self.host = host
        self.port = port

# Create instances with validation
config = ServerConfig(
    host=StringType("localhost"),
    port=PortNumber(8080)
)
```

## Development

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`
4. Run type checks: `poetry run mypy src tests`

## License

MIT License
