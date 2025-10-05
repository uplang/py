# UP Parser for Python

[![PyPI version](https://badge.fury.io/py/up-lang.svg)](https://pypi.org/project/up-lang/)
[![CI](https://github.com/uplang/py/workflows/CI/badge.svg)](https://github.com/uplang/py/actions)
[![Documentation Status](https://readthedocs.org/projects/uplang/badge/?version=latest)](https://uplang.readthedocs.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Official Python implementation of the UP (Unified Properties) language parser.

📚 **[API Documentation](https://uplang.readthedocs.io/)** | 🧪 **[Test Status](https://github.com/uplang/py/actions)** | 📖 **[Specification](https://github.com/uplang/spec)**

> **Pythonic Design** - Uses dataclasses, type hints, and Python best practices

## Features

- ✅ **Full UP Syntax Support** - Scalars, blocks, lists, tables, multiline strings
- ✅ **Type Annotations** - Parse and preserve type hints (`!int`, `!bool`, etc.)
- ✅ **Type Hints** - Full Python type annotations with mypy support
- ✅ **Dataclasses** - Modern Python 3.7+ features
- ✅ **Well-Tested** - Comprehensive pytest test suite
- ✅ **Zero Dependencies** - Pure Python implementation
- ✅ **CLI Tool** - Command-line utility included

## Requirements

- Python 3.7 or later

## Installation

```bash
# From PyPI
pip install up-lang

# From source
git clone https://github.com/uplang/py
cd py
pip install -e .
```

## Quick Start

```python
from up_parser import Parser

# Create a parser
parser = Parser()

# Parse UP content
doc = parser.parse("""
name Alice
age!int 30
config {
  debug!bool true
}
""")

# Access values
print(doc.get_scalar('name'))  # 'Alice'

# Iterate nodes
for node in doc.nodes:
    print(f"{node.key} = {node.value}")
```

**📖 For detailed examples and tutorials, see [QUICKSTART.md](QUICKSTART.md)**

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Getting started guide with examples
- **[DESIGN.md](DESIGN.md)** - Architecture and design decisions
- **[UP Specification](https://github.com/uplang/spec)** - Complete language specification

## API Overview

### Core Classes

- **`Parser`** - Main parser for converting UP text into documents
- **`Document`** - Parsed document with convenient access methods
- **`Node`** - Dataclass for key-value pairs with optional type annotation
- **`Value`** - Union type for all value types (scalar, block, list, table)

### Basic Usage

```python
from up_parser import Parser

parser = Parser()

# Parse from string
doc = parser.parse(content)

# Parse from file
with open('config.up') as f:
    doc = parser.parse_file(f)

# Access values
name = doc.get_scalar('name')
server = doc.get_block('server')
tags = doc.get_list('tags')
```

**See [DESIGN.md](DESIGN.md) for complete API documentation and implementation details.**

## CLI Tool

```bash
# Parse and display
up-parse config.up

# Validate syntax
up-validate config.up

# Convert to JSON
up-convert config.up --format json
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=up_parser

# Run specific test
pytest tests/test_parser.py::test_simple_scalars
```

## Project Structure

```
py/
├── up_parser/
│   ├── __init__.py
│   ├── parser.py        # Main parser implementation
│   ├── types.py         # Data structures and types
│   └── cli.py           # CLI tool
├── tests/
│   └── test_parser.py   # Comprehensive tests
├── setup.py
├── README.md            # This file
├── QUICKSTART.md        # Getting started guide
├── DESIGN.md            # Architecture documentation
└── LICENSE              # GNU GPLv3
```

## Contributing

Contributions are welcome! Please see the main [CONTRIBUTING.md](https://github.com/uplang/spec/blob/main/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Links

- **[UP Language Specification](https://github.com/uplang/spec)** - Official language spec
- **[Syntax Reference](https://github.com/uplang/spec/blob/main/SYNTAX-REFERENCE.md)** - Quick syntax guide
- **[UP Namespaces](https://github.com/uplang/ns)** - Official namespace plugins

### Other Implementations

- **[Go](https://github.com/uplang/go)** - Reference implementation
- **[Java](https://github.com/uplang/java)** - Modern Java 21+ with records and sealed types
- **[JavaScript/TypeScript](https://github.com/uplang/js)** - Browser and Node.js support
- **[Rust](https://github.com/uplang/rust)** - Zero-cost abstractions and memory safety
- **[C](https://github.com/uplang/c)** - Portable C implementation

## Support

- **Issues**: [github.com/uplang/py/issues](https://github.com/uplang/py/issues)
- **Discussions**: [github.com/uplang/spec/discussions](https://github.com/uplang/spec/discussions)
