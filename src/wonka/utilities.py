"""Shared tools.

Contents:


To Do:


"""
from __future__ import annotations

import inspect
import pathlib
import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def _drop_prefix_from_str(item: str, /, prefix: str, divider: str = '') -> str:
    """Drops `prefix` from `item` with `divider` in between.

    Args:
        item (str): item to be modified.
        prefix (str): prefix to be added to `item`.
        divider (str): str to add between `item` and `prefix`. Defaults to '',
            which means no divider will be added.

    Returns:
        str: modified str.

    """
    prefix = ''.join([prefix, divider])
    if item.startswith(prefix):
        return item[len(prefix):]
    else:
        return item

def _drop_suffix_from_str(item: str, /, suffix: str, divider: str = '') -> str:
    """Drops `suffix` from `item` with `divider` in between.

    Args:
        item (str): item to be modified.
        suffix (str): suffix to be added to 'item'.

    Returns:
        str: modified str.

    """
    suffix = ''.join([suffix, divider])
    if item.endswith(suffix):
        return item.removesuffix(suffix)
    else:
        return item

def _iterify(item: Any) -> Iterable:
    """Returns `item` as an iterable, but does not iterate str types.

    Args:
        item (Any): item to turn into an iterable

    Returns:
        Iterable: of `item`. A str type will be stored as a single item in an
            Iterable wrapper.

    """
    if item is None:
        return iter(())
    elif isinstance(item, (str, bytes)):
        return iter([item])
    else:
        try:
            return iter(item)
        except TypeError:
            return iter((item,))

def _namify(item: Any, /, default: str | None = None) -> str | None:
    """Returns str name representation of 'item'.

    Args:
        item (Any): item to determine a str name.
        default(Optional[str]): default name to return if other methods at name
            creation fail.

    Returns:
        str: a name representation of 'item.'

    """
    if isinstance(item, str):
        return item
    elif (
        hasattr(item, 'name')
        and not inspect.isclass(item)
        and isinstance(item.name, str)):
        return item.name
    else:
        try:
            return _snakify(item.__name__)
        except AttributeError:
            if item.__class__.__name__ is not None:
                return _snakify(item.__class__.__name__)
            else:
                return default

def _snakify(item: str) -> str:
    """Converts a capitalized str to snake case.

    Args:
        item (str): str to convert.

    Returns:
        str: 'item' converted to snake case.

    """
    item = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()

def _pathlibify(item: str | pathlib.Path) -> pathlib.Path:
    """Converts string `path` to pathlib.Path object.

    Args:
        item: either a string of a path or a pathlib.Path object.

    Raises:
        TypeError if `path` is neither a str or pathlib.Path type.

    Returns:
        pathlib.Path object.

    """
    if isinstance(item, str):
        return pathlib.Path(item)
    elif isinstance(item, pathlib.Path):
        return item
    else:
        raise TypeError('item must be str or pathlib.Path type')


def _typify(item: str) -> list[Any] | int | float | bool | str:
    """Converts stings to appropriate, supported datatypes.

    The method converts strings to list (if ', ' is present), int, float,
    or bool datatypes based upon the content of the string. If no
    alternative datatype is found, the item is returned in its original
    form.

    Args:
        item (str): string to be converted to appropriate datatype.

    Returns:
        list[Any] | int | float | bool | str: converted item.

    """
    if not isinstance(item, str):
        return item
    else:
        try:
            return int(item)
        except ValueError:
            try:
                return float(item)
            except ValueError:
                if item.lower() in ['true', 'yes']:
                    return True
                elif item.lower() in ['false', 'no']:
                    return False
                elif ', ' in item:
                    item = item.split(', ')
                    return [_typify(i) for i in item]
                else:
                    return item

def _is_sequence(
    item: Any,
    include_str: bool = False,
    raise_error: bool | None = None) -> bool:
    """Returns if 'item' is a sequence.

    If 'exclude_str' is True (the default) and 'item' is a str, False will be
    returned.

    Args:
        item (Any): object to examine.
        include_str (bool): whether to return True if 'item' is a str.

    Returns:
        bool: if 'item' is a sequence.

    """
    if not inspect.isclass(item):
        item = item.__class__
    return (
        issubclass(item, Sequence)
        and (not issubclass(item, str) or include_str))