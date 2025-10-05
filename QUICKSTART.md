# Quick Start Guide - Python

Get started with the UP Parser for Python in 5 minutes!

## Installation

```bash
pip install up-lang
```

## Your First Program

Create `example.py`:

```python
from up_parser import Parser

# Create a parser
parser = Parser()

# Parse UP content
doc = parser.parse("""
name Alice
age!int 30
active!bool true
""")

# Access values
print('Name:', doc.get_scalar('name'))
print('Age:', doc.get_scalar('age'))

# Iterate all nodes
for node in doc.nodes:
    print(f"{node.key} = {node.value}")
```

Run it:

```bash
python example.py
```

## Common Use Cases

### 1. Configuration Files

```python
from up_parser import Parser

with open('config.up') as f:
    doc = Parser().parse_file(f)
    
# Access configuration
server = doc.get_block('server')
if server:
    print('Host:', server.get('host'))
    print('Port:', server.get('port'))
```

### 2. Type Hints

```python
from up_parser import Parser, Document, Node
from typing import Optional

parser: Parser = Parser()
doc: Document = parser.parse(input)

name: Optional[str] = doc.get_scalar('name')
```

### 3. Working with Blocks

```python
doc = parser.parse("""
database {
  host db.example.com
  port!int 5432
}
""")

db = doc.get_block('database')
print(f"Database: {db['host']}:{db['port']}")
```

## Next Steps

- Read the [DESIGN.md](DESIGN.md) for implementation details
- Explore the [UP Specification](https://github.com/uplang/spec)
- Check out [example files](https://github.com/uplang/spec/tree/main/examples)

## Need Help?

- 📚 [Full Documentation](README.md)
- 💬 [Discussions](https://github.com/uplang/spec/discussions)
- 🐛 [Report Issues](https://github.com/uplang/py/issues)
