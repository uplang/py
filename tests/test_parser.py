import pytest
from uplang import parse, Parser, Document, ParseError


def test_parse_empty_string():
    doc = parse("")
    assert doc.is_empty()
    assert len(doc.nodes) == 0


def test_parse_simple_scalar():
    doc = parse("name John Doe")
    assert len(doc.nodes) == 1
    assert doc.nodes[0].key == "name"
    assert doc.nodes[0].value == "John Doe"


def test_parse_type_annotation():
    doc = parse("age!int 30")
    assert len(doc.nodes) == 1
    assert doc.nodes[0].key == "age"
    assert doc.nodes[0].type_annotation == "int"
    assert doc.nodes[0].value == "30"


def test_parse_multiple_key_values():
    doc = parse("name John Doe\nage!int 30")
    assert len(doc.nodes) == 2
    assert doc.nodes[0].key == "name"
    assert doc.nodes[1].key == "age"


def test_skip_comments():
    doc = parse("# Comment\nname John\n# Another comment\nage 30")
    assert len(doc.nodes) == 2


def test_parse_block():
    doc = parse("server {\nhost localhost\nport!int 8080\n}")
    assert len(doc.nodes) == 1
    assert doc.nodes[0].key == "server"
    assert isinstance(doc.nodes[0].value, dict)
    assert doc.nodes[0].value["host"] == "localhost"


def test_parse_list():
    doc = parse("fruits [\napple\nbanana\ncherry\n]")
    assert len(doc.nodes) == 1
    assert doc.nodes[0].key == "fruits"
    assert isinstance(doc.nodes[0].value, list)
    assert len(doc.nodes[0].value) == 3


def test_parse_inline_list():
    doc = parse("colors [red, green, blue]")
    assert len(doc.nodes) == 1
    assert isinstance(doc.nodes[0].value, list)
    assert len(doc.nodes[0].value) == 3
    assert doc.nodes[0].value[0] == "red"


def test_parse_multiline():
    doc = parse("description ```\nLine 1\nLine 2\n```")
    assert len(doc.nodes) == 1
    assert "Line 1" in doc.nodes[0].value
    assert "Line 2" in doc.nodes[0].value


def test_parser_instance():
    parser = Parser()
    assert parser is not None


def test_document():
    doc = Document()
    assert doc.is_empty()
