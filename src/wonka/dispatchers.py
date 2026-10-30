"""Dispatchers: factory classes that call other constructors.

Contents:
    Delegate (`base.Factory`): builds classes and/or instances using methods
        that follow a naming convention and the `str` names of the types of the
        first argument passed to the `create` class method.
    Sourcerer (`base.Factory`, `abc.ABC`): builds classes and/or instances
        using methods that follow a naming convention (set at
        `options._METHOD_NAMER`) and a `dict` of types stored in the `sources`
        class attribute.

"""

from __future__ import annotations

import abc
import dataclasses
import inspect
from typing import TYPE_CHECKING, Any, ClassVar

from . import base, options, shared

if TYPE_CHECKING:
    from collections.abc import Callable, MutableMapping


@dataclasses.dataclass
class Delegate(base.Factory):
    """Builds based on the `str` name of the type passed.

    This factory acts as a dispatcher to call creation methods based on the type
    or name of the type passed in a manner similar to `Sourcerer`. However,
    unlike `Sourcerer`, `Delegate` only finds a matching creation method if the
    `str` name of the type of `item` matches a substring of the creation method
    name using the format of `options._METHOD_NAMER`. A `str` item is not named
    by its type: the `str` itself is used as the name (so `'ini'` calls the
    `from_ini` method with `'ini'`).

    """

    """ Class Methods """

    @classmethod
    def create(
            cls,
            item: Any,
            parameters: base.Parameters | None = None,
            **kwargs: base.Kwargs) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        Args:
            item: data for construction of the returned item.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            **kwargs: keyword arguments passed to the creation method.

        Raises:
            AttributeError: if an appropriate method does not exist for the
                data type of `item`.

        Returns:
            Created item.

        """
        builder = _get_creation_method_name(item)
        item = _get_from_builder_method(
            factory = cls,
            method = builder,
            source = item,
            **kwargs)
        return shared.finalize(item = item, parameters = parameters)


@dataclasses.dataclass
class Sourcerer(base.Factory, abc.ABC):
    """Builds based on compatibility with keys in the `sources` class attribute.

    This factory acts as a dispatcher to call other methods based on the type
    passed. Unlike `Delegate`, `Sourcerer` is more forgiving by allowing the
    type passed to be a subtype or instance of the type listed as a key in the
    `sources` class attribute. The keys of `sources` are checked in order, so
    more specific types should be listed before more general ones.

    The name for a `Sourcerer` is spelled the way it is instead of "Sorcerer"
    because the `sources` attribute is used. This is inspired by the "Divinity:
    Original Sin" games where the magic users are called "Sourcerers" because
    they may manipulate the magical energy known as "source".
    https://divinity.fandom.com/wiki/Sourcerer

    Attributes:
        sources: `dict` with keys that are types and values are substrings of
            the names of methods to call when the key type is passed to the
            `create` method. Defaults to an empty `dict`.

    """

    sources: ClassVar[MutableMapping[type[Any], str]] = {}

    """ Class Methods """

    @classmethod
    def create(
            cls,
            item: Any,
            parameters: base.Parameters | None = None,
            **kwargs: base.Kwargs) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        Args:
            item: data for construction of the returned item.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            **kwargs: keyword arguments passed to the creation method.

        Raises:
            AttributeError: if the value matching the key `item` does not
                correspond to a method in the `Sourcerer` subclass.
            KeyError: if there is no key in `sources` matching the type for
                `item`.

        Returns:
            Created item.

        """
        for kind, substring in cls.sources.items():
            if _is_kind(item, kind):
                builder = _get_creation_method_name(substring)
                item = _get_from_builder_method(
                    factory = cls,
                    method = builder,
                    source = item,
                    **kwargs)
                return shared.finalize(item = item, parameters = parameters)
        message = f'{item} does not match any recognized types'
        raise KeyError(message)


""" Private Functions """


def _get_creation_method_name(
        source: Any,
        method_namer: Callable[[Any], str] | None = None) -> str:
    """Returns the creation method name for factories that call other methods.

    Args:
        source: source data for creating a method name.
        method_namer: callable to create the creation method name. Defaults to
            `None`. If it is `None`, the global namer stored in
            `options._METHOD_NAMER` will be used.

    Returns:
        Name of the creation method to use.

    """
    if not isinstance(source, str):
        source = options._KEY_NAMER(source)
    namer = method_namer or options._METHOD_NAMER
    return namer(source)


def _get_from_builder_method(
        factory: Any,
        method: str,
        source: Any,
        **kwargs: base.Kwargs) -> Any:
    """Returns constructed item from a builder method of `factory`.

    Args:
        factory: factory class or instance.
        method: name of the method to use to construct an item.
        source: the `source` data used to create item.
        **kwargs: keyword arguments passed to the builder method.

    Raises:
        AttributeError: if `factory` has no method named `method`.

    Returns:
        Constructed item.

    """
    try:
        builder = getattr(factory, method)
    except AttributeError as error:
        message = f'{method} does not exist in {factory}'
        raise AttributeError(message) from error
    return builder(source, **kwargs)


def _is_kind(item: Any, kind: type[Any]) -> bool:
    """Returns if `item` is an instance or subclass of `kind`.

    Args:
        item: item to evaluate.
        kind: type to compare `item` to.

    Returns:
        Whether `item` is an instance or subclass of `kind`.

    """
    return (
        isinstance(item, kind)
        or (inspect.isclass(item) and issubclass(item, kind)))
