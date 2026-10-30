"""Tests the `wonka` constructor storage classes."""

from __future__ import annotations

import dataclasses
from typing import Any, ClassVar

import pytest
from conftest import Adder, Doubler

import wonka


@dataclasses.dataclass
class Options(wonka.Subclasser):
    """Base `Subclasser` for the tests."""


@dataclasses.dataclass
class Settings(Options):
    """Intermediate subclass of `Options`."""


@dataclasses.dataclass
class Configuration(Settings):
    """Indirect subclass of `Options` with stored contents.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)


@dataclasses.dataclass
class RegistrationDesk(wonka.Registrar):
    """`Registrar` with a fixed registry."""

    registry: ClassVar[dict[str, Any]] = {'configuration': Configuration}


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


def test_manufacturer() -> None:
    """Tests creating items with constructors stored in a `Manufacturer`."""
    depot = wonka.Manufacturer()
    depot.add(Options)
    depot.add({'registration': RegistrationDesk})
    setup = depot['options'].create(
        'configuration',
        parameters = {'contents': {'processors': 8}})
    assert setup.contents['processors'] == 8
    assert isinstance(setup, Configuration)
    registration = depot['registration'].create(
        'configuration',
        parameters = {'contents': {'tree': 'house'}})
    assert registration.contents['tree'] == 'house'
    assert isinstance(registration, Configuration)


def test_add_validation() -> None:
    """Tests that `add` rejects anything that is not a constructor."""
    depot = wonka.Manufacturer()
    with pytest.raises(TypeError):
        depot.add(3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        depot.add({'ok': Adder, 'bad': 3})  # type: ignore[dict-item]
    assert len(depot) == 0


def test_add_manager_instance() -> None:
    """Tests that a `Manager` instance can be stored."""
    depot = wonka.Manufacturer()
    depot.add({'line': wonka.Assembler([Adder, Doubler])})
    assert depot['line'].create(1) == 4


def test_add_uses_global_keyer() -> None:
    """Tests that `add` names a single constructor with the global keyer."""
    wonka.set_keyer(lambda x: x.__name__.upper())
    depot = wonka.Manufacturer()
    depot.add(Adder)
    assert depot.keys() == ('ADDER',)


def test_add_duck_type_with_relaxed_compatibility() -> None:
    """Tests that relaxed compatibility allows other classes with `create`."""
    depot = wonka.Manufacturer()
    with pytest.raises(TypeError):
        depot.add(Duck)  # type: ignore[arg-type]
    wonka.set_compatibility_rule(False)
    depot.add(Duck)  # type: ignore[arg-type]
    assert depot['duck'] is Duck


def test_mapping_interface() -> None:
    """Tests the `dict`-like methods of `Manufacturer`."""
    depot = wonka.Manufacturer()
    depot.add(Adder)
    depot.add({'doubler': Doubler})
    assert depot.keys() == ('adder', 'doubler')
    assert depot.values() == (Adder, Doubler)
    assert depot.items() == (('adder', Adder), ('doubler', Doubler))
    assert depot['adder'] is Adder
    assert list(depot) == ['adder', 'doubler']
    del depot['adder']
    assert len(depot) == 1
    with pytest.raises(KeyError):
        del depot['adder']
    with pytest.raises(KeyError):
        depot.delete('adder')


def test_setitem() -> None:
    """Tests setting a constructor with a key."""
    depot = wonka.Manufacturer()
    depot['x'] = Adder
    assert depot['x'] is Adder


def test_add_operator_returns_copy() -> None:
    """Tests that `+` returns a new instance and leaves both unchanged."""
    depot = wonka.Manufacturer({'adder': Adder})
    combined = depot + Doubler
    assert combined is not depot
    assert combined.keys() == ('adder', 'doubler')
    assert depot.keys() == ('adder',)
    assert isinstance(combined, wonka.Manufacturer)
    mapping = {'d': Doubler}
    assert (depot + mapping).keys() == ('adder', 'd')
    assert mapping == {'d': Doubler}


def test_add_operator_validates() -> None:
    """Tests that `+` raises the same errors as `add`."""
    depot = wonka.Manufacturer()
    with pytest.raises(TypeError):
        depot + 3  # type: ignore[operator]


def test_inplace_add_operator() -> None:
    """Tests that `+=` adds to the instance in place."""
    depot = wonka.Manufacturer()
    original = depot
    depot += Adder
    depot += {'doubler': Doubler}
    assert depot is original
    assert depot.keys() == ('adder', 'doubler')


def test_subset() -> None:
    """Tests `subset` with `include`, `exclude`, or both."""
    depot = wonka.Manufacturer(
        {'adder': Adder, 'doubler': Doubler, 'options': Options})
    assert depot.subset(include = 'adder').keys() == ('adder',)
    assert depot.subset(exclude = 'adder').keys() == ('doubler', 'options')
    assert depot.subset(
        include = ['adder', 'doubler'],
        exclude = ['doubler']).keys() == ('adder',)
    assert depot.keys() == ('adder', 'doubler', 'options')


def test_subset_returns_new_instance() -> None:
    """Tests that `subset` does not share `contents` with the original."""
    depot = wonka.Manufacturer({'adder': Adder})
    subset = depot.subset(include = 'adder')
    assert subset is not depot
    subset['doubler'] = Doubler
    assert depot.keys() == ('adder',)


def test_subset_errors() -> None:
    """Tests that `subset` raises errors for missing or absent arguments."""
    depot = wonka.Manufacturer({'adder': Adder})
    with pytest.raises(ValueError, match = 'include or exclude'):
        depot.subset()
    with pytest.raises(KeyError):
        depot.subset(include = 'missing')


if __name__ == '__main__':
    test_manufacturer()
