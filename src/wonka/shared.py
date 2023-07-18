"""Shared business logic functions for wonka.

Contents:
    finalize: finalizes construction before returning a value, including calling
        the 'produce' method of the passed item.
    inject_attributes: adds keys and values of a mapping to a class or instance
        as attributes.
    is_constructor: returns boolean as to whether an item is a wonka-compatible
        constructor.

"""
from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from . import base, configuration

if TYPE_CHECKING:
    from collections.abc import Hashable, MutableMapping


def finalize(
    item: Any,
    parameters: MutableMapping[Hashable, Any] | None = None,
    factory: type[base.Factory] | None = None) -> Any:
    """Modifies 'item' and possibly incorporates 'parameters'.

    Args:
        item (Any): item created by a factory that may need to be altered
            before being returned by the factory 'create' method.
        parameters: Optional[MutableMapping[Hashable, Any]]: keyword
            arguments to pass or add to a created instance. Defaults to
            None.
        factory (Optional[Type[base.Factory]]): the factory used to create
            'item'. This need not be passed if 'item' is also the factory for
            its creation. Defaults to None. If 'factory' is None, this function
            will look for an 'produce' method on item.


    Returns:
        Any: modified item.

    """
    factory = factory or item
    if (hasattr(factory, 'produce') and inspect.ismethod(factory.produce)):
        return factory.produce(item, parameters)
    else:
        return item if parameters is None else item(**parameters)

def inject_attributes(
    item: Any,
    parameters: MutableMapping[Hashable, Any] | None = None,
    overwrite: bool | None = None) -> Any:
    """Manages 'item' and possibly incorporates 'parameters'.

    Args:
        item (Any): item to have 'parameters' injected.
        parameters: Optional[MutableMapping[Hashable, Any]]: keyword arguments
            to add to a created instance. Defaults to None.
        overwrite (Optional[bool]): whether to overwrite existing attributes,
            if they exist. Defaults to None. If the value is None, the global
            _OVERWRITE setting will be used.


    Returns:
        Any: modified item.

    """
    if parameters:
        overwrite = configuration._OVERWRITE if overwrite is None else overwrite
        for key, value in parameters.items():
            if overwrite or not hasattr(item, key):
                setattr(item, key, value)
    return item

def is_constructor(item: Any) -> bool:
    """Returns if 'item' is a wonka-compatible constructor.

    If the global '_STRICT_COMPATIBILITY' setting is True, this function uses a
    narrow definition of 'constructor' to only include:
        1) subclasses or instances of Factory; or
        2) subclasss instances of Manager.
    If '_STRICT_COMPATIBILITY' is False, the function merely tests whether
    'item' has a 'create' method.

    Args:
        item (Any): item to test

    Returns:
        bool: whether 'item' is a wonka-compatible constructor

    """
    if configuration._STRICT_COMPATIBILITY:
        return (
            (inspect.isclass(item) and issubclass(item, base.Factory))
            or isinstance(item, base.Manager | base.Factory))
    else:
        return (
            hasattr(item, 'create')
            and inspect.ismethod(item.create))
