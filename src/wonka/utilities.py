"""Shared tools.

Contents:


To Do:


"""
from __future__ import annotations

import inspect
import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def _iterify(item: Any) -> Iterable:
    """Returns `item` as an iterable, but does not iterate `str` types.

    Args:
        item: item to turn into an iterable.

    Returns:
        Iterable of `item`. A `str` type will be stored as a single item in an
            iterable wrapper.

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
    """Returns `str` name representation of `item`.

    Args:
        item: item to determine a `str` name for.
        default: default name to return if a name cannot be created.

    Returns:
        A name representation of `item.`

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
    """Converts a capitalized `str` to snake case.

    Args:
        item: `str` to convert.

    Returns:
        `item` converted to snake case.

    """
    item = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()

def _is_sequence(
    item: Any, *,
    include_str: bool = False) -> bool:
    """Returns if `item` is a sequence.

    If `exclude_str` is True (the default) and `item` is a str, False will be
    returned.

    Args:
        item: object to examine.
        include_str: whether to return True if `item` is a `str`.

    Returns:
        Whether an `item` is a sequence.

    """
    if not inspect.isclass(item):
        item = item.__class__
    return (
        issubclass(item, Sequence)
        and (not issubclass(item, str) or include_str))
