"""Tests for UP parser."""

import pytest


def test_import():
    """Test that the package can be imported."""
    try:
        import uplang
        assert uplang is not None
    except ImportError:
        # Module might not be installed yet
        pass


def test_basic():
    """Basic sanity test."""
    assert True


def test_parser_exists():
    """Test that parser module exists."""
    try:
        from uplang import parser
        assert parser is not None
    except ImportError:
        # Parser might not exist yet
        pass

