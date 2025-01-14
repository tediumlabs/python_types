"""Core types for the tedium type system.

This module provides both immutable and mutable variants of core types.
Import the specific variant you need:

    from tedium.types.core import Integer  # immutable
    from tedium.types.core import MutableInteger  # mutable
"""

from .base import BaseType

__all__ = [
    'BaseType',
]

# Types will be added to __all__ as they are implemented
