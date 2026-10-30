"""Tests the `wonka` base classes."""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest
from conftest import Adder

import wonka
from wonka import base


@dataclasses.dataclass
class Counter(wonka.Manager):
    """Manager that counts its constructors.

    Args:
        contents: stored constructors. Defaults to an empty list.

    """

    contents: list[Any] = dataclasses.field(default_factory = list)

    def manage(self, item: Any, **kwargs: Any) -> Any:
        """Returns `item` and the number of stored constructors.

        Args:
            item: item to return.
            **kwargs: ignored keyword arguments.

        Returns:
            A `tuple` of `item` and the length of `contents`.

        """
        return item, len(self.contents)


def test_base_classes_are_abstract() -> None:
    """Tests that the base classes cannot be instanced."""
    with pytest.raises(TypeError):
        base.Factory()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        base.Manager([])  # type: ignore[abstract]
    with pytest.raises(TypeError):
        base.Producer()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        base.Cluster()  # type: ignore[abstract]


def test_manager_create_calls_manage() -> None:
    """Tests that `Manager.create` is an alias for `manage`."""
    counter = Counter([Adder, Adder])
    assert counter.create('x') == ('x', 2)
    assert counter.manage('x') == ('x', 2)


def test_manager_iterates_contents() -> None:
    """Tests that iterating a `Manager` iterates its `contents`."""
    assert list(Counter([Adder])) == [Adder]


def test_manager_is_constructor() -> None:
    """Tests that a `Manager` instance is a `wonka` constructor."""
    assert wonka.is_constructor(Counter())
    assert not wonka.is_constructor(Counter)


def test_manufacturer_is_cluster() -> None:
    """Tests that `Manufacturer` is a `Cluster` subclass."""
    assert issubclass(wonka.Manufacturer, wonka.Cluster)
