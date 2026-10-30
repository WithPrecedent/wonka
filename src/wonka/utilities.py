"""Private tools used throughout `wonka`.

Every function in this module is private and documented in its own docstring.

"""

from __future__ import annotations

import inspect
import pathlib
import re
from collections.abc import Iterator
from typing import Any

""" Private Functions """


def _iterify(item: Any) -> Iterator[Any]:
    """Returns `item` as an iterator, but does not iterate `str` types.

    Args:
        item: item to turn into an iterator.

    Returns:
        Iterator of `item`. `None` becomes an empty iterator. A `str` or `bytes`
            type (or any non-iterable) is wrapped so that it is returned as a
            single item.

    """
    if item is None:
        return iter(())
    if isinstance(item, str | bytes):
        return iter([item])
    try:
        return iter(item)
    except TypeError:
        return iter((item,))


def _namify(item: Any) -> str:
    """Returns `str` name representation of `item`.

    A `str` is returned as is. An instance with a `str` `name` attribute
    returns that attribute. Otherwise, the snake case name of `item` (if it is
    a class or function) or of its class (if it is an instance) is returned.

    Args:
        item: item to determine a `str` name for.

    Returns:
        A name representation of `item`.

    """
    if isinstance(item, str):
        return item
    if (
            hasattr(item, 'name')
            and not inspect.isclass(item)
            and isinstance(item.name, str)):
        return item.name
    try:
        return _snakify(item.__name__)
    except AttributeError:
        return _snakify(item.__class__.__name__)


def _pathlibify(item: str | pathlib.Path) -> pathlib.Path:
    """Converts a `str` path to a `pathlib.Path` type.

    Args:
        item: item to convert, if it is not already a `pathlib.Path` type.

    Returns:
        `item` converted to `pathlib.Path`.

    Raises:
        TypeError: if `item` is neither a `str` nor a `pathlib.Path` type.

    """
    if isinstance(item, pathlib.Path):
        return item
    if isinstance(item, str):
        return pathlib.Path(item)
    message = 'item must be a str or pathlib.Path type'
    raise TypeError(message)


def _snakify(item: str) -> str:
    """Converts a capitalized `str` to snake case.

    Args:
        item: `str` to convert.

    Returns:
        `item` converted to snake case.

    """
    item = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', item).lower()
