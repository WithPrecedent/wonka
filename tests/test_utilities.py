"""Tests the private `wonka` utilities."""

from __future__ import annotations

import pathlib

import pytest
from conftest import Thing

from wonka import utilities


def test_snakify() -> None:
    """Tests converting capitalized names to snake case."""
    assert utilities._snakify('HTTPServer') == 'http_server'
    assert utilities._snakify('FastPlugin') == 'fast_plugin'
    assert utilities._snakify('already_snake') == 'already_snake'


def test_namify() -> None:
    """Tests naming `str` types, classes, instances, and functions."""
    assert utilities._namify('abc') == 'abc'
    assert utilities._namify(Thing) == 'thing'
    assert utilities._namify(Thing()) == 'thing'
    assert utilities._namify(test_snakify) == 'test_snakify'
    assert utilities._namify(3) == 'int'


def test_namify_uses_name_attribute() -> None:
    """Tests that an instance with a `str` `name` attribute uses it."""

    class Named:
        """Class with a `name` attribute."""

        name = 'given'

    class BadName:
        """Class with a `name` attribute that is not a `str`."""

        name = 3

    assert utilities._namify(Named()) == 'given'
    assert utilities._namify(Named) == 'named'
    assert utilities._namify(BadName()) == 'bad_name'


def test_iterify() -> None:
    """Tests wrapping items in an iterator."""
    assert list(utilities._iterify(None)) == []
    assert list(utilities._iterify('abc')) == ['abc']
    assert list(utilities._iterify(b'abc')) == [b'abc']
    assert list(utilities._iterify(5)) == [5]
    assert list(utilities._iterify([1, 2])) == [1, 2]
    assert list(utilities._iterify(i for i in (1, 2))) == [1, 2]


def test_pathlibify() -> None:
    """Tests converting `str` paths to `pathlib.Path`."""
    assert utilities._pathlibify('a/b') == pathlib.Path('a/b')
    path = pathlib.Path('x')
    assert utilities._pathlibify(path) is path
    with pytest.raises(TypeError):
        utilities._pathlibify(3)  # type: ignore[arg-type]
