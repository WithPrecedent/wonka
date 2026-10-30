"""Tests the `wonka` dispatcher factories."""

from __future__ import annotations

import dataclasses
from collections.abc import MutableMapping
from typing import Any, ClassVar, NoReturn

import pytest

import wonka
from wonka import dispatchers


@dataclasses.dataclass
class Settings(wonka.Delegate):
    """`Delegate` that is created from a `dict`.

    Args:
        contents: stored settings. Defaults to an empty `dict`.
        label: optional label. Defaults to `None`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)
    label: str | None = None

    @classmethod
    def from_dict(
            cls,
            item: dict[str, Any],
            label: str | None = None) -> Settings:
        """Returns a `Settings` instance from a `dict`.

        Args:
            item: settings to store.
            label: optional label. Defaults to `None`.

        Returns:
            A `Settings` instance.

        """
        return cls(contents = item, label = label)


@dataclasses.dataclass
class Configuration(wonka.Sourcerer):
    """`Sourcerer` that is created from a mapping."""

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)
    sources: ClassVar[dict[Any, str]] = {MutableMapping: 'dictionary'}

    @classmethod
    def from_dictionary(cls, item: dict[str, Any]) -> Configuration:
        """Returns a `Configuration` instance from a `dict`.

        Args:
            item: settings to store.

        Returns:
            A `Configuration` instance.

        """
        return cls(contents = item)


@dataclasses.dataclass
class Maker(wonka.Sourcerer):
    """`Sourcerer` with several sources.

    Args:
        value: stored value. Defaults to `None`.

    """

    value: Any = None
    sources: ClassVar[dict[Any, str]] = {
        bool: 'flag',
        int: 'number',
        MutableMapping: 'mapping',
        str: 'text',
        type: 'kind'}

    @classmethod
    def from_flag(cls, item: bool) -> Maker:
        """Returns a `Maker` from a `bool`.

        Args:
            item: value to store.

        Returns:
            A `Maker` instance.

        """
        return cls(value = ('flag', item))

    @classmethod
    def from_number(cls, item: int) -> Maker:
        """Returns a `Maker` from an `int`.

        Args:
            item: value to store.

        Returns:
            A `Maker` instance.

        """
        return cls(value = item)

    @classmethod
    def from_mapping(cls, item: MutableMapping[str, Any]) -> Maker:
        """Returns a `Maker` from a mapping.

        Args:
            item: value to store.

        Returns:
            A `Maker` instance.

        """
        return cls(value = dict(item))

    @classmethod
    def from_text(cls, item: str) -> Maker:
        """Returns a `Maker` from a `str`.

        Args:
            item: value to store.

        Returns:
            A `Maker` instance.

        """
        return cls(value = item)

    @classmethod
    def from_kind(cls, item: type[Any]) -> Maker:
        """Returns a `Maker` from a class.

        Args:
            item: class whose name is stored.

        Returns:
            A `Maker` instance.

        """
        return cls(value = item.__name__)


@dataclasses.dataclass
class Broken(wonka.Sourcerer):
    """`Sourcerer` with a missing method and a method that fails."""

    sources: ClassVar[dict[Any, str]] = {int: 'missing', str: 'boom'}

    @classmethod
    def from_boom(cls, item: str) -> NoReturn:
        """Raises an `AttributeError`.

        Args:
            item: ignored item.

        Raises:
            AttributeError: always.

        """
        message = 'internal failure'
        raise AttributeError(message)


def test_delegate() -> None:
    """Tests that `Delegate` calls the method named after the item's type."""
    contents = {'tree': 'house', 'ghost': 'town'}
    settings = Settings.create(contents)
    assert settings.contents['tree'] == 'house'
    assert isinstance(settings, Settings)


def test_delegate_passes_kwargs_and_parameters() -> None:
    """Tests that `Delegate` passes kwargs and injects `parameters`."""
    settings = Settings.create({'a': 1}, label = 'given')
    assert settings.label == 'given'
    settings = Settings.create({'a': 1}, parameters = {'label': 'injected'})
    assert settings.label == 'injected'


def test_delegate_no_method() -> None:
    """Tests that `Delegate` raises an error for an unsupported type."""
    with pytest.raises(AttributeError, match = 'from_int'):
        Settings.create(1)


def test_delegate_uses_global_method_namer() -> None:
    """Tests that `Delegate` uses the global method namer."""

    @dataclasses.dataclass
    class Builder(wonka.Delegate):
        """`Delegate` with a custom method naming convention."""

        @classmethod
        def make_int(cls, item: int) -> int:
            """Returns `item` negated.

            Args:
                item: `int` to negate.

            Returns:
                `item` negated.

            """
            return -item

    wonka.set_method_namer(lambda x: f'make_{x}')
    assert Builder.create(3) == -3


def test_delegate_str_item_names_method() -> None:
    """Tests that a `str` item is the name used for the creation method."""
    settings = Settings.create('dict')
    assert settings.contents == 'dict'


def test_sourcerer() -> None:
    """Tests that `Sourcerer` calls the method for a matching source."""
    contents = {'tree': 'house', 'ghost': 'town'}
    configuration = Configuration.create(contents)
    assert configuration.contents['tree'] == 'house'
    assert isinstance(configuration, Configuration)


def test_sourcerer_skips_non_matching_kinds() -> None:
    """Tests that `Sourcerer` checks every source until one matches."""
    assert Maker.create('hi').value == 'hi'
    assert Maker.create({'a': 1}).value == {'a': 1}
    assert Maker.create(3).value == 3


def test_sourcerer_checks_sources_in_order() -> None:
    """Tests that the first matching source is used."""
    assert Maker.create(True).value == ('flag', True)


def test_sourcerer_matches_subclasses() -> None:
    """Tests that classes match sources that they are subclasses of."""

    class Count(int):
        """Subclass of `int`."""

    assert Maker.create(Count).value is Count
    assert Maker.create(Maker).value == 'Maker'


def test_sourcerer_no_match() -> None:
    """Tests that `Sourcerer` raises a `KeyError` without a match."""
    with pytest.raises(KeyError, match = 'does not match'):
        Maker.create(3.5)


def test_missing_builder_method() -> None:
    """Tests that a missing builder method raises an `AttributeError`."""
    with pytest.raises(AttributeError, match = 'from_missing'):
        Broken.create(1)


def test_builder_attribute_error_not_masked() -> None:
    """Tests that an `AttributeError` inside a builder is not replaced."""
    with pytest.raises(AttributeError, match = 'internal failure'):
        Broken.create('x')


def test_is_kind() -> None:
    """Tests `_is_kind` with instances and classes."""
    assert dispatchers._is_kind(bool, int)
    assert dispatchers._is_kind(True, int)
    assert not dispatchers._is_kind('x', int)
    assert not dispatchers._is_kind(str, int)


def test_get_creation_method_name() -> None:
    """Tests naming creation methods with the default and a custom namer."""
    assert dispatchers._get_creation_method_name('text') == 'from_text'
    assert dispatchers._get_creation_method_name({}) == 'from_dict'
    name = dispatchers._get_creation_method_name(
        'text',
        method_namer = lambda x: f'build_{x}')
    assert name == 'build_text'


if __name__ == '__main__':
    test_delegate()
    test_sourcerer()
