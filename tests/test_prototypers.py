"""Tests the `wonka` prototyper factories."""

from __future__ import annotations

import dataclasses

from conftest import Thing

import wonka


@dataclasses.dataclass
class Clone(wonka.Scribe):
    """`Scribe` with default contents.

    Args:
        contents: stored contents.

    """

    contents: dict[str, str] = dataclasses.field(
        default_factory = lambda: {'tree': 'house', 'ghost': 'town'})


def test_scribe() -> None:
    """Tests that a `Scribe` clones itself without an item."""
    clone_class = Clone.create()
    clone_instance = clone_class()
    assert clone_instance.contents['tree'] == 'house'
    assert isinstance(clone_instance, Clone)
    new_clone_instance = Clone.create(parameters = {})
    assert new_clone_instance.contents['ghost'] == 'town'
    assert isinstance(new_clone_instance, Clone)


def test_scribe_none_clones_self() -> None:
    """Tests that a deep copy of a class is the class itself."""
    assert Clone.create() is Clone


def test_scribe_clones_falsy_items() -> None:
    """Tests that falsy items are cloned instead of the `Scribe`."""
    assert wonka.Scribe.create(0) == 0
    assert wonka.Scribe.create('') == ''
    assert wonka.Scribe.create([]) == []


def test_scribe_deep_copies() -> None:
    """Tests that a `Scribe` makes a deep copy."""
    original = [[1], [2]]
    copied = wonka.Scribe.create(original)
    assert copied == original
    assert copied is not original
    assert copied[0] is not original[0]


def test_scribe_injects_parameters_into_copy() -> None:
    """Tests that `parameters` change the copy but not the original."""
    original = Thing(value = 1)
    copied = wonka.Scribe.create(original, parameters = {'value': 2})
    assert copied.value == 2
    assert original.value == 1


if __name__ == '__main__':
    test_scribe()
