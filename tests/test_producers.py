"""Tests the `wonka` producer mixins."""

from __future__ import annotations

import dataclasses
import inspect
from typing import Any

from conftest import Thing

import wonka


@dataclasses.dataclass
class Configuration(wonka.Classer, wonka.Delegate):
    """`Delegate` that always returns a class.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Configuration:
        """Returns a `Configuration` instance from a `dict`.

        Args:
            item: settings to store.

        Returns:
            A `Configuration` instance.

        """
        return cls(contents = item)


@dataclasses.dataclass
class Settings(wonka.Flexer, wonka.Delegate):
    """`Delegate` that returns an instance only with parameters.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Settings:
        """Returns a `Settings` instance from a `dict`.

        Args:
            item: settings to store.

        Returns:
            A `Settings` instance.

        """
        return cls(contents = item)

    @classmethod
    def from_list(cls, item: list[Any]) -> type[Settings]:
        """Returns the `Settings` class, ignoring `item`.

        Args:
            item: ignored `list`.

        Returns:
            The `Settings` class.

        """
        return cls


@dataclasses.dataclass
class Setup(wonka.Instancer, wonka.Delegate):
    """`Delegate` that always returns an instance.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Setup:
        """Returns a `Setup` instance from a `dict`.

        Args:
            item: settings to store.

        Returns:
            A `Setup` instance.

        """
        return cls(contents = item)

    @classmethod
    def from_list(cls, item: list[Any]) -> type[Setup]:
        """Returns the `Setup` class, ignoring `item`.

        Args:
            item: ignored `list`.

        Returns:
            The `Setup` class.

        """
        return cls


def test_classer() -> None:
    """Tests that a `Classer` factory returns a class."""
    config = Configuration.create({'tree': 'house'})
    assert config is Configuration


def test_flexer() -> None:
    """Tests that a `Flexer` factory returns what its method creates."""
    settings = Settings.create({'tree': 'house'})
    assert not inspect.isclass(settings)
    assert Settings.create([]) is Settings


def test_flexer_with_parameters() -> None:
    """Tests that a `Flexer` factory returns an instance with parameters."""
    settings = Settings.create([], parameters = {'contents': {'a': 1}})
    assert isinstance(settings, Settings)
    assert settings.contents == {'a': 1}


def test_instancer() -> None:
    """Tests that an `Instancer` factory always returns an instance."""
    assert isinstance(Setup.create({'tree': 'house'}), Setup)
    assert isinstance(Setup.create([]), Setup)
    setup = Setup.create([], parameters = {'contents': {'a': 1}})
    assert setup.contents == {'a': 1}


def test_producers_directly() -> None:
    """Tests calling the `produce` methods directly."""
    thing = Thing()
    assert wonka.Classer.produce(thing) is Thing
    assert wonka.Classer.produce(Thing) is Thing
    assert wonka.Classer.produce(Thing, {'value': 3}) is Thing
    assert wonka.Instancer.produce(Thing) == Thing()
    assert wonka.Instancer.produce(Thing, {'value': 3}).value == 3
    assert wonka.Instancer.produce(thing) is thing
    assert wonka.Flexer.produce(Thing) is Thing
    assert wonka.Flexer.produce(Thing, {'value': 5}).value == 5
    assert wonka.Flexer.produce(thing, {'value': 6}) is thing
    assert thing.value == 6
    assert wonka.Instancer.produce(thing, {'value': 7}) is thing
    assert thing.value == 7


if __name__ == '__main__':
    test_classer()
    test_flexer()
    test_instancer()
