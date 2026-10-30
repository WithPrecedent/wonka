"""Factory classes that utilize explicit or implicit registries.

Contents:
    Registrar (`base.Factory`): builds classes and/or instances from a registry
        stored in the `registry` class attribute.
    AutoRegistrar (`Registrar`, `abc.ABC`): `Registrar` that automatically
        registers its subclasses.
    Subclasser (`base.Factory`, `abc.ABC`): builds classes and/or instances
        from the `__subclasses__` method and a dynamically created registry
        based upon it.

"""

from __future__ import annotations

import abc
import copy
import dataclasses
from typing import TYPE_CHECKING, Any, ClassVar

from . import base, options, shared

if TYPE_CHECKING:
    from collections.abc import Hashable, Mapping


@dataclasses.dataclass
class Registrar(base.Factory):
    """Builds an item from a registry.

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[base.GenericDict] = {}

    """ Class Methods """

    @classmethod
    def create(
            cls,
            item: Hashable,
            parameters: base.Parameters | None = None,
            **kwargs: base.Kwargs) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        Args:
            item: name corresponding to a key in `registry`.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            **kwargs: allows subclass to take kwargs.

        Raises:
            KeyError: if a corresponding item in `registry` does not exist for
                `item`.

        Returns:
            Created item.

        """
        item = _get_from_registry(item = item, registry = cls.registry)
        return shared.finalize(item = item, parameters = parameters)


@dataclasses.dataclass
class AutoRegistrar(Registrar, abc.ABC):
    """`Registrar` that automatically registers its subclasses.

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[base.GenericDict] = {}

    """ Initialization Methods """

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically registers subclasses.

        Each direct subclass of `AutoRegistrar` that does not define its own
        `registry` gets a new one so that unrelated class families do not share
        (and pollute) a single registry. Deeper subclasses register in the
        registry they inherit.

        Args:
            **kwargs: keyword arguments passed to the parent class
                `__init_subclass__` method.

        """
        super().__init_subclass__(**kwargs)
        if cls.registry is AutoRegistrar.registry:
            cls.registry = {}
        cls.registry[options._KEY_NAMER(cls)] = cls


@dataclasses.dataclass
class Subclasser(base.Factory, abc.ABC):
    """Builds a subclass without requiring a storage attribute.

    Unlike some other factories, this one does not require any class attributes.
    Instead, it relies on pre-existing data and lazily adds keys to create
    a registry facade.

    This factory uses the subclasses stored in `__subclasses__` class method
    that is automatically created with every class. It creates a `dict` on the
    fly with key names based on `options._KEY_NAMER`. Because of this,
    `Subclasser` should ordinarily be used as a mixin (although it could simply
    be subclassed, if you prefer).

    """

    """ Class Methods """

    @classmethod
    def create(
            cls,
            item: Hashable,
            parameters: base.Parameters | None = None,
            **kwargs: base.Kwargs) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        A subclass in the `__subclasses__` class method is selected based on the
        naming convention in `options._KEY_NAMER`.

        Args:
            item: name of the subclass to create.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            **kwargs: allows subclass to take kwargs.

        Raises:
            KeyError: if a corresponding subclass does not exist for `item`.

        Returns:
            Created item.

        """
        keyer = options._KEY_NAMER
        registry = {keyer(s): s for s in _get_all_subclasses(cls)}
        item = _get_from_registry(item = item, registry = registry)
        return shared.finalize(item = item, parameters = parameters)


""" Private Functions """


def _get_all_subclasses(item: type[Any]) -> list[type[Any]]:
    """Returns a list of all subclasses of `item`, including indirect ones.

    Each subclass appears once, in the order in which it is first found by a
    depth-first search of `__subclasses__`.

    Args:
        item: class for which to find subclasses.

    Returns:
        List of all subclasses of `item`.

    """
    subclasses: dict[type[Any], None] = {}
    for subclass in item.__subclasses__():
        subclasses[subclass] = None
        subclasses.update(dict.fromkeys(_get_all_subclasses(subclass)))
    return list(subclasses)


def _get_from_registry(item: Hashable, registry: Mapping[Any, Any]) -> Any:
    """Returns a copy of a stored item in `registry` with the key of `item`.

    Args:
        item: key for item sought in `registry`.
        registry: registry where the sought item is stored.

    Raises:
        KeyError: if `item` does not match any key in `registry`.

    Returns:
        A deep copy of an item stored in `registry`.

    """
    try:
        return copy.deepcopy(registry[item])
    except KeyError as error:
        message = f'{item} was not found in the registry'
        raise KeyError(message) from error
