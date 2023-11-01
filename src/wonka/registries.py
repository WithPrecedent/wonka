"""Factory classes that utilize explicit or implicit registries.

Contents:
    Registrar (`base.Factory`): builds classes and/or instances from a registry
        stored in the `registry` class attribute.
    Subclasser (base.Factory, abc.ABC): builds classes and/or instances from the
        `__subclasses__` method and a dynamically created registry based upon
        it.

"""
from __future__ import annotations

import abc
import copy
import dataclasses
from typing import TYPE_CHECKING, Any, ClassVar

from . import base, configuration, shared

if TYPE_CHECKING:
    from collections.abc import Hashable, MutableMapping


@dataclasses.dataclass
class Registrar(base.Factory):
    """Builds an item from a registry.

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[MutableMapping[Hashable, Any]] = ""

    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Hashable,
        parameters: MutableMapping[Hashable, Any] | None = None) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        Args:
            item (Hashable): name corresponding to a key in `registry`.
            parameters: keyword arguments to pass or add to a created instance.

        Raises:
            KeyError: If a corresponding item in `registry` does not exist for
                `item.`

        Returns:
            Any: created item.

        """
        item = _get_from_registry(item = item, registry = cls.registry)
        return shared.finalize(item = item, parameters = parameters)


@dataclasses.dataclass
class Subclasser(base.Factory, abc.ABC):
    """Builds a subclass without requiring a storage attribute.

    Unlike some other factories, this one does not require any class attributes.
    Instead, it relies on pre-existing data and lazily adds keys to create
    a registry facade.

    This factory uses the subclasses stored in `__subclasses__` class method
    that is automatically created with every class. It creates a `dict` on the
    fly with key names based on `configuration._KEY_NAMER`. Because of this,
    `Subclasser` should ordinarily be used as a mixin (although it could simply
    be subclassed, if you prefer).

    """

    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Any,
        parameters: MutableMapping[Hashable, Any] | None = None,
        **kwargs: Any) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        A subclass in the `__subclasses__` class method is selected based on the
        naming convention in `wonka._KEY_NAMER`.

        Args:
            item: data for construction of the returned item.
            parameters: keyword arguments to pass or add to a created instance.
            kwargs: allows subclass to take kwargs.

        Raises:
            KeyError: If a corresponding subclass does not exist for `item.`

        Returns:
            Any: created item.

        """
        keyer = configuration._KEY_NAMER
        all_subclasses = _get_all_subclasses(cls)
        registry = {keyer(s): s for s in all_subclasses}
        item = _get_from_registry(item = item, registry = registry)
        return shared.finalize(item = item, parameters = parameters)


def _get_from_registry(
    item: Hashable,
    registry: MutableMapping[Hashable, Any]) -> Any:
    """Returns a copy of a stored item in `registry` with the key of `item`.

    Args:
        item (Hashable): key for item sought in `registry`.
        registry: registry where the sought item is stored.

    Raises:
        KeyError: if `item` does not match any key in `registry`.

    Returns:
        Any: a deep copy of an item stored in `registry`.

    """
    try:
        return copy.deepcopy(registry[item])
    except KeyError as e:
        raise KeyError(f'{item} was not found in the registry') from e

def _get_all_subclasses(item: type[Any]) -> list[type[Any]]:
    """Returns a list of all subclasses of `items`, including indirect ones.

    Args:
        item: class for which to find subclasses.

    Returns:
        List of all subclasses of `item`.

    """
    return list(set(item.__subclasses__()).union(
        [s for c in item.__subclasses__() for s in _get_all_subclasses(c)]))
