# Design Documentation - Python Implementation

This document describes the architecture and design decisions of the Python UP parser implementation.

## Overview

The Python implementation prioritizes:

- **Pythonic** - Follows Python best practices and idioms
- **Type Hints** - Full typing support with mypy
- **Dataclasses** - Modern Python 3.7+ features
- **Simple** - Clean, readable code
- **Zero Dependencies** - Pure Python

## Architecture

### Data Structures

```python
@dataclass
class Node:
    key: str
    type: str  # Optional, empty if not specified
    value: Value

@dataclass
class Document:
    nodes: List[Node]
    
    def get_scalar(self, key: str) -> Optional[str]: ...
    def get_block(self, key: str) -> Optional[Dict[str, Value]]: ...
    def get_list(self, key: str) -> Optional[List[Value]]: ...
```

### Value Types

```python
Value = Union[
    str,                    # Scalar
    Dict[str, 'Value'],     # Block
    List['Value'],          # List
    Table,                  # Table
    str                     # Multiline
]
```

## Parser Implementation

### Single-Pass Parsing

Line-by-line parsing with state management:

```python
class Parser:
    def parse(self, content: str) -> Document:
        lines = content.splitlines()
        nodes = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            if self._is_empty(line) or self._is_comment(line):
                i += 1
                continue
            
            node, next_i = self._parse_line(lines, i)
            nodes.append(node)
            i = next_i
        
        return Document(nodes)
```

## Type System

### Type Hints

Full typing support:

```python
from typing import Optional, List, Dict, Union

def get_scalar(self, key: str) -> Optional[str]:
    for node in self.nodes:
        if node.key == key and isinstance(node.value, str):
            return node.value
    return None
```

## Design Decisions

### Why Dataclasses?

**Pros:**
- Less boilerplate
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints by default
- Python 3.7+ standard

**Decision:** Modern Python best practice

### Why Dict for Blocks?

**Pros:**
- Native type
- Familiar to Python developers
- Built-in operations
- JSON serializable

**Decision:** Simplicity over custom classes

## Contributing

When contributing to the Python implementation:

1. **Type hints** - All public APIs
2. **PEP 8** - Follow Python style guide
3. **Tests** - pytest with >90% coverage
4. **Docstrings** - Google style

## References

- [UP Specification](https://github.com/uplang/spec)
- [PEP 8](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
