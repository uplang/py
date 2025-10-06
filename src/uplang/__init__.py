"""UP (Unified Properties) parser for Python.

A modern, human-friendly data serialization format parser.

Example:
    >>> from uplang import parse
    >>>
    >>> doc = parse('''
    ... name John Doe
    ... age!int 30
    ... ''')
    >>> doc.nodes[0].key
    'name'
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__version__ = "1.0.0"
__all__ = ["parse", "Parser", "Document", "Node", "ParseError"]


# Type aliases
Block = dict[str, Any]
List = list[Any]


@dataclass(slots=True)
class Node:
    """A key-value node with optional type annotation."""

    key: str
    value: Any
    type_annotation: str | None = None


@dataclass(slots=True)
class Document:
    """Represents a parsed UP document."""

    nodes: list[Node] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if document is empty."""
        return len(self.nodes) == 0


class ParseError(Exception):
    """Parse error."""

    pass


class Parser:
    """UP document parser with configurable behavior."""

    def parse_document(self, input_text: str) -> Document:
        """Parse a UP document from a string."""
        lines = input_text.split("\n")
        nodes: list[Node] = []
        i = 0

        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            # Skip empty lines and comments
            if not trimmed or trimmed.startswith("#"):
                i += 1
                continue

            # Skip stray closing braces (shouldn't happen in well-formed docs)
            if trimmed in ("}", "]"):
                i += 1
                continue

            try:
                node, next_i = self._parse_line(lines, i)
                nodes.append(node)
                i = next_i
            except Exception as e:
                raise ParseError(f"line {i + 1}: {e}") from e

        return Document(nodes=nodes)

    def _parse_line(self, lines: list[str], start_index: int) -> tuple[Node, int]:
        """Parse a single line."""
        line = lines[start_index]
        key_part, val_part = self._split_key_value(line)
        key, type_annotation = self._parse_key_and_type(key_part)

        value, next_index = self._parse_value(lines, start_index, val_part, type_annotation)

        return Node(key=key, value=value, type_annotation=type_annotation), next_index

    def _split_key_value(self, line: str) -> tuple[str, str]:
        """Split a line into key and value parts."""
        parts = line.split(None, 1)
        if len(parts) < 2:
            return parts[0] if parts else "", ""
        return parts[0], parts[1]

    def _parse_key_and_type(self, key_part: str) -> tuple[str, str | None]:
        """Extract key and type annotation from the key part."""
        if "!" in key_part:
            key, type_ann = key_part.split("!", 1)
            return key, type_ann
        return key_part, None

    def _parse_value(
        self,
        lines: list[str],
        start_index: int,
        val_part: str,
        type_annotation: str | None,
    ) -> tuple[Any, int]:
        """Parse the value part based on its format."""
        # Multiline string
        if val_part.startswith("```"):
            return self._parse_multiline(lines, start_index + 1, type_annotation)

        # Block
        if val_part == "{":
            return self._parse_block(lines, start_index + 1)

        # List
        if val_part == "[":
            return self._parse_list(lines, start_index + 1)

        # Inline list
        if val_part.startswith("[") and val_part.endswith("]"):
            return self._parse_inline_list(val_part), start_index + 1

        # Scalar
        return val_part, start_index + 1

    def _parse_multiline(
        self, lines: list[str], start_index: int, type_annotation: str | None
    ) -> tuple[str, int]:
        """Parse a multiline string (triple backticks)."""
        content: list[str] = []
        i = start_index

        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            if trimmed == "```":
                i += 1
                break

            content.append(line)
            i += 1

        text = "\n".join(content)

        # Apply dedenting if type annotation is a number
        if type_annotation and type_annotation.isdigit():
            dedent_amount = int(type_annotation)
            text = self._dedent(text, dedent_amount)

        return text, i

    def _parse_block(self, lines: list[str], start_index: int) -> tuple[Block, int]:
        """Parse a block (nested key-value pairs)."""
        block: Block = {}
        i = start_index

        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            if trimmed == "}":
                i += 1
                break

            # Skip empty lines and comments
            if not trimmed or trimmed.startswith("#"):
                i += 1
                continue

            node, next_i = self._parse_line(lines, i)
            block[node.key] = node.value
            i = next_i

        return block, i

    def _parse_list(self, lines: list[str], start_index: int) -> tuple[List, int]:
        """Parse a list."""
        lst: List = []
        i = start_index

        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            if trimmed == "]":
                i += 1
                break

            # Skip empty lines and comments
            if not trimmed or trimmed.startswith("#"):
                i += 1
                continue

            # Inline list within multiline list
            if trimmed.startswith("[") and trimmed.endswith("]"):
                lst.append(self._parse_inline_list(trimmed))
                i += 1
            # Nested block
            elif trimmed == "{":
                block, next_i = self._parse_block(lines, i + 1)
                lst.append(block)
                i = next_i
            # Scalar
            else:
                lst.append(trimmed)
                i += 1

        return lst, i

    def _parse_inline_list(self, s: str) -> List:
        """Parse an inline list [item1, item2, ...]."""
        content = s.strip()[1:-1]  # Remove [ and ]

        if not content.strip():
            return []

        return [item.strip() for item in content.split(",")]

    def _dedent(self, text: str, amount: int) -> str:
        """Remove N spaces from the beginning of each line."""
        lines = text.split("\n")
        return "\n".join(line[amount:] if len(line) >= amount else line for line in lines)


def parse(input_text: str) -> Document:
    """Parse UP document from a string (convenience function)."""
    return Parser().parse_document(input_text)
