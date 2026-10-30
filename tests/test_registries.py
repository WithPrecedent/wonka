"""Tests the `wonka` registry factories."""

from __future__ import annotations

import dataclasses
from typing import Any, ClassVar

import pytest
from conftest import Thing

import wonka
from wonka import registries


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
class Setup(Settings):
    """Another indirect subclass of `Options`."""


@dataclasses.dataclass
class RegistrationDesk(wonka.Registrar):
    """`Registrar` with a fixed registry."""

    registry: ClassVar[dict[str, Any]] = {
        'configuration': Configuration,
        'setup': Setup,
        'thing': Thing(value = 1)}


@dataclasses.dataclass
class Plugin(wonka.AutoRegistrar):
    """`AutoRegistrar` family for the tests.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)


@dataclasses.dataclass
class FastPlugin(Plugin):
    """Direct subclass of `Plugin`."""


@dataclasses.dataclass
class SlowPlugin(FastPlugin):
    """Indirect subclass of `Plugin`."""


@dataclasses.dataclass
class Gadget(wonka.AutoRegistrar):
    """Second `AutoRegistrar` family for the tests."""


@dataclasses.dataclass
class Widget(Gadget):
    """Direct subclass of `Gadget`."""


""" Registrar """


def test_registrar() -> None:
    """Tests creating an instance from a registered class."""
    config = RegistrationDesk.create(
        'configuration',
        parameters = {'contents': {'processors': 8}})
    assert config.contents['processors'] == 8
    assert isinstance(config, Configuration)


def test_registrar_without_parameters_returns_class() -> None:
    """Tests that a registered class is returned without parameters."""
    assert RegistrationDesk.create('setup') is Setup


def test_registrar_returns_copy_of_instance() -> None:
    """Tests that changing a returned instance does not change the registry."""
    thing = RegistrationDesk.create('thing', parameters = {'value': 2})
    assert thing.value == 2
    assert RegistrationDesk.registry['thing'].value == 1


def test_registrar_accepts_kwargs() -> None:
    """Tests that `create` accepts extra keyword arguments."""
    assert RegistrationDesk.create('setup', extra = True) is Setup


def test_registrar_missing_key() -> None:
    """Tests that a missing key raises a `KeyError` with the key."""
    with pytest.raises(KeyError, match = 'nope'):
        RegistrationDesk.create('nope')


""" Subclasser """


def test_subclasser() -> None:
    """Tests creating an instance of an indirect subclass."""
    setup = Options.create(
        'configuration',
        parameters = {'contents': {'processors': 8}})
    assert setup.contents['processors'] == 8
    assert isinstance(setup, Configuration)


def test_subclasser_indirect_and_missing() -> None:
    """Tests direct, indirect, and missing subclasses."""
    assert Options.create('setup') is Setup
    assert isinstance(Options.create('settings', {}), Settings)
    with pytest.raises(KeyError):
        Options.create('options')


def test_subclasser_from_intermediate_class() -> None:
    """Tests that only subclasses of the calling class are found."""
    assert Settings.create('setup') is Setup
    with pytest.raises(KeyError):
        Settings.create('settings')


def test_get_all_subclasses_has_no_duplicates() -> None:
    """Tests that a class with two parents in the family appears once."""

    class Top:
        """Top of a diamond inheritance."""

    class Left(Top):
        """Left side of a diamond inheritance."""

    class Right(Top):
        """Right side of a diamond inheritance."""

    class Bottom(Left, Right):
        """Bottom of a diamond inheritance."""

    subclasses = registries._get_all_subclasses(Top)
    assert subclasses == [Left, Bottom, Right]


""" AutoRegistrar """


def test_auto_registrar_registers_indirect_subclasses() -> None:
    """Tests that direct and indirect subclasses are registered."""
    assert Plugin.registry['fast_plugin'] is FastPlugin
    assert Plugin.registry['slow_plugin'] is SlowPlugin
    assert Plugin.registry['plugin'] is Plugin


def test_auto_registrar_families_do_not_share_registries() -> None:
    """Tests that each family gets its own registry."""
    assert Plugin.registry is not Gadget.registry
    assert wonka.AutoRegistrar.registry == {}
    assert 'widget' in Gadget.registry
    assert 'widget' not in Plugin.registry
    assert 'fast_plugin' not in Gadget.registry


def test_auto_registrar_create() -> None:
    """Tests creating classes and instances from the registry."""
    plugin = Plugin.create('fast_plugin', parameters = {'contents': {'a': 1}})
    assert isinstance(plugin, FastPlugin)
    assert plugin.contents == {'a': 1}
    assert Plugin.create('slow_plugin') is SlowPlugin
    with pytest.raises(KeyError):
        Plugin.create('nope')


def test_auto_registrar_custom_keyer() -> None:
    """Tests that the global keyer names registered subclasses."""
    wonka.set_keyer(lambda x: f'k_{x.__name__}')

    @dataclasses.dataclass
    class Custom(Plugin):
        """Subclass registered with a custom key."""

    assert Plugin.registry['k_Custom'] is Custom


def test_auto_registrar_own_registry() -> None:
    """Tests that a direct subclass with its own registry keeps it."""
    own: dict[str, Any] = {}

    @dataclasses.dataclass
    class Tool(wonka.AutoRegistrar):
        """`AutoRegistrar` family with a predefined registry."""

        registry: ClassVar[dict[str, Any]] = own

    assert Tool.registry is own
    assert own == {'tool': Tool}


if __name__ == '__main__':
    test_registrar()
    test_subclasser()
