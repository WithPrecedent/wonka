"""Stores groups of `wonka` constructors.

Contents:
    Manufacturer (`base.Cluster`): `dict`-like class that stores `wonka`
        constructors. Has an `add` method that validates any added values as
        `wonka` compatible.

"""

from __future__ import annotations

import copy
import dataclasses
from collections.abc import Iterable, Mapping
from typing import Self

from . import base, options, shared, utilities


@dataclasses.dataclass
class Manufacturer(base.Cluster):
    """`dict`-like container of factories.

    A `Manufacturer` may serve as a one-stop spot for factories. Each factory
    need not be of the same subtype, as long as they pass the `is_constructor`
    test. The use of a `Manufacturer` is wholly optional - it is just a
    convenience offered by `wonka`. To access individual constructors, the
    following format should be used:

    ```python
    manufacturer_instance['constructor_name'].create(*args, **kwargs)
    ```

    Args:
        contents: stored `dict` of `wonka` factories. Defaults to an empty
            `dict`.

    """

    contents: base.ConstructorDict = dataclasses.field(default_factory = dict)

    """ Public Methods """

    def add(
            self,
            item: base.ConstructorDict | base.Constructor,
            **kwargs: base.Kwargs) -> None:
        """Adds `item` to the `contents` attribute.

        If `item` is a single constructor, its key is created by the global
        `_KEY_NAMER` function in `options`.

        Args:
            item: factory or factories to add.
            **kwargs: allows subclass to take other keyword arguments.

        Raises:
            TypeError: if all of the values of `item` are not `wonka`-compatible
                factories or if `item` itself is not a `wonka`-compatible
                factory.

        """
        if isinstance(item, Mapping):
            if not all(shared.is_constructor(v) for v in item.values()):
                message = (
                    'All values in item must be wonka-compatible constructors')
                raise TypeError(message)
            self.contents.update(item)
        elif shared.is_constructor(item):
            self.contents[options._KEY_NAMER(item)] = item
        else:
            message = (
                'item must either be a wonka-compatible constructor or a dict-'
                'like object with values that are constructors')
            raise TypeError(message)

    def delete(self, item: str, **kwargs: base.Kwargs) -> None:
        """Deletes `item` in `contents`.

        Args:
            item: key in `contents` to delete the key/value pair.
            **kwargs: allows subclass to take other keyword arguments.

        Raises:
            KeyError: if `item` is not a key in `contents`.

        """
        del self.contents[item]

    def items(self) -> tuple[tuple[str, base.Constructor], ...]:
        """Emulates Python `dict` `items` method.

        Returns:
            A `tuple` equivalent to `dict.items()`.

        """
        return tuple(self.contents.items())

    def keys(self) -> tuple[str, ...]:
        """Returns `contents` keys as a `tuple`.

        Returns:
            A `tuple` equivalent to `dict.keys()`.

        """
        return tuple(self.contents.keys())

    def subset(
            self,
            include: str | Iterable[str] | None = None,
            exclude: str | Iterable[str] | None = None) -> Self:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is `None`, all existing items will be added to the new subset
        class instance before `exclude` is applied. Like the `subset` method of
        `Assembler`, the new instance is a deep copy.

        Args:
            include: key(s) to include in the new `Manufacturer` instance.
                Defaults to `None`.
            exclude: key(s) to exclude from the new `Manufacturer` instance.
                Defaults to `None`.

        Raises:
            KeyError: if a key in `include` is not in `contents`.
            ValueError: if `include` and `exclude` are both `None`.

        Returns:
            New instance with only keys from `include` and no keys in `exclude`.

        """
        if include is None and exclude is None:
            message = 'include or exclude must not be None'
            raise ValueError(message)
        if include is None:
            contents = dict(self.contents)
        else:
            contents = {
                k: self.contents[k] for k in utilities._iterify(include)}
        if exclude is not None:
            excluded = set(utilities._iterify(exclude))
            contents = {k: v for k, v in contents.items() if k not in excluded}
        new_manufacturer = copy.copy(self)
        new_manufacturer.contents = copy.deepcopy(contents)
        return new_manufacturer

    def values(self) -> tuple[base.Constructor, ...]:
        """Returns `contents` values as a `tuple`.

        Returns:
            A `tuple` equivalent to `dict.values()`.

        """
        return tuple(self.contents.values())
