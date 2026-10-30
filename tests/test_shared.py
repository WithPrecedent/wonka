"""Tests the shared `wonka` functions."""

from __future__ import annotations

from typing import Any

from conftest import Adder, Thing

import wonka


class Duck:
    """Class with a `create` class method that is not a `wonka` class."""

    @classmethod
    def create(cls, item: Any) -> Any:
        """Returns `item`.

        Args:
            item: item to return.

        Returns:
            `item`, unchanged.

        """
        return item


class InstanceDuck:
    """Class with a `create` instance method."""

    def create(self, item: Any) -> Any:
        """Returns `item`.

        Args:
            item: item to return.

        Returns:
            `item`, unchanged.

        """
        return item


def test_finalize_class_with_parameters() -> None:
    """Tests that a class is instanced with `parameters`."""
    assert wonka.finalize(Thing, {'value': 4}).value == 4


def test_finalize_instance_with_parameters() -> None:
    """Tests that `parameters` are injected into an instance."""
    thing = Thing()
    result = wonka.finalize(thing, {'value': 9})
    assert result is thing
    assert thing.value == 9


def test_finalize_without_parameters() -> None:
    """Tests that an item is returned unchanged without `parameters`."""
    assert wonka.finalize(Thing) is Thing


def test_finalize_uses_produce_of_item() -> None:
    """Tests that the `produce` method of `item` is used."""

    class Made(wonka.Classer):
        """`Classer` subclass that is its own item."""

    assert wonka.finalize(Made(), {'ignored': True}) is Made


def test_finalize_uses_produce_of_factory() -> None:
    """Tests that the `produce` method of `factory` is used."""
    result = wonka.finalize(Thing, factory = wonka.Instancer)
    assert result == Thing()


def test_inject_attributes_overwrite_rules() -> None:
    """Tests the `overwrite` argument and empty `parameters`."""
    thing = Thing(value = 1)
    wonka.inject_attributes(thing, {'value': 2}, overwrite = False)
    assert thing.value == 1
    wonka.inject_attributes(thing, {'value': 2}, overwrite = True)
    assert thing.value == 2
    assert wonka.inject_attributes(thing, None) is thing
    assert wonka.inject_attributes(thing, {}) is thing


def test_inject_attributes_uses_global_overwrite_rule() -> None:
    """Tests that the global overwrite rule is used by default."""
    thing = Thing(value = 1)
    wonka.set_overwrite_rule(False)
    wonka.inject_attributes(thing, {'value': 2, 'extra': 3})
    assert thing.value == 1
    assert thing.extra == 3  # type: ignore[attr-defined]
    wonka.set_overwrite_rule(True)
    wonka.inject_attributes(thing, {'value': 2})
    assert thing.value == 2


def test_is_constructor_strict() -> None:
    """Tests strict compatibility, which requires `wonka` classes."""
    assert wonka.is_constructor(wonka.Scribe)
    assert wonka.is_constructor(Adder())
    assert wonka.is_constructor(wonka.Assembler())
    assert not wonka.is_constructor(Duck)
    assert not wonka.is_constructor(3)


def test_is_constructor_relaxed() -> None:
    """Tests relaxed compatibility, which allows any `create` method."""
    wonka.set_compatibility_rule(False)
    assert wonka.is_constructor(Duck)
    assert wonka.is_constructor(InstanceDuck())
    assert not wonka.is_constructor(InstanceDuck)
    assert not wonka.is_constructor(3)
