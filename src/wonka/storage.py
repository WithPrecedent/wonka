"""Stores groups of `wonka` constructors.

Contents:
    Manufacturer: `dict`-like class that stores `wonka` constructors. Has an
        `add` method that validates any added values as `wonka` compatible.

"""
from __future__ import annotations

import copy
import dataclasses
from collections.abc import Hashable, Iterator, MutableMapping, Sequence
from typing import Any

from . import base, configuration, shared, utilities


@dataclasses.dataclass
class Manufacturer(MutableMapping):
    """`dict`-like container of factories.

    A `Manufacturer` may serve as a one-stop spot for factories. Each factory
    need not be of the same subtype, as they pass the `is_constructor` test. The
    use of a `Manufacturer` is wholly optional - it is just a convenience
    offered by `wonka`. To access individual constructors, the following format
    should be used:

    ```python
    manufacturer_instance['constructor_name'].create(*args, **kwargs)
    ```

    Args:
        contents: stored `dict` of `wonka` factories. Defaults to an empty
            `dict`.

    """

    contents: MutableMapping[Hashable, base.Constructor] = dataclasses.field(
        default_factory = dict)

    """ Class Methods """

    @classmethod
    def fromkeys(
        cls,
        keys: Sequence[Hashable],
        value: Any,
        **kwargs: Any) -> Manufacturer:
        """Emulates the `fromkeys` class method from a python `dict`.

        Args:
            keys: items to be keys in a new `Manufacturer`.
            value: the value to use for all values in a new `Manufacturer`.
            kwargs: additional arguments to pass to `dict.fromkeys`.

        Returns:
            Instance formed from `keys` and `value`.

        """
        return cls(contents = dict.fromkeys(keys, value), **kwargs)

    """ Instance Methods """

    def add(
        self,
        item: MutableMapping[
            Hashable, base.Constructor] | base.Constructor) -> None:
        """Adds `item` to the `contents` attribute.

        Args:
            item: factory or factories to add.

        Raises:
            TypeError: if all of the values of `item` are not `wonka`-compatible
                factories or if `item` itself is not a `wonka`-compatible
                factory.

        """
        if isinstance(item, MutableMapping):
            if all(shared.is_constructor(v) for v in item.values()):
                self.contents.update(item)
            else:
                message = (
                    'All values in item must be wonka-compatible constructors')
                raise TypeError(message)
        elif shared.is_constructor(item):
            key = configuration._KEY_NAMER(item)
            self.contents.update({key: item})
        else:
            message = (
                'item must either be a wonka-compatible constructor or a dict-'
                'like object with values that are constructors')
            raise TypeError(message)

    def delete(self, item: Hashable) -> None:
        """Deletes `item` in `contents`.

        Args:
            item: key in `contents` to delete the key/value pair.

        """
        del self.contents[item]
        return

    def items(self) -> tuple[tuple[Hashable, Any], ...]:
        """Emulates Python `dict` `items` method.

        Returns:
            A `tuple` equivalent to `dict.items()`.

        """
        return tuple(zip(self.keys(), self.values()))

    def keys(self) -> tuple[Hashable, ...]:
        """Returns `contents` keys as a `tuple`.

        Returns:
            A `tuple` equivalent to `dict.keys()`.

        """
        return tuple(self.contents.keys())

    def subset(
        self,
        include: Hashable | Sequence[Hashable] | None = None,
        exclude: Hashable | Sequence[Hashable] | None = None) -> Manufacturer:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is None, all existing items will be added to the new subset
        class instance before `exclude` is applied.

        Args:
            include: key(s) to include in the new `Manufacturer` instance.
            exclude: key(s) to exclude from the new `Manufacturer` instance.

        Raises:
            ValueError: if `include` and `exclude` are both None.

        Returns:
            New instance with only keys from `include` and no keys in `exclude`.

        """
        if include is None and exclude is None:
            message = 'either the include or exclude argument must not be None'
            raise ValueError(message)
        else:
            if include is None:
                contents = copy.deepcopy(self.contents)
            else:
                include = list(utilities._iterify(include))
                contents = {k: self.contents[k] for k in include}
            if exclude is not None:
                exclude = list(utilities._iterify(exclude))
                contents = {
                    k: v for k, v in contents.items()
                    if k not in exclude}
            new_dictionary = copy.deepcopy(self)
            new_dictionary.contents = contents
        return new_dictionary

    def values(self) -> tuple[Any, ...]:
        """Returns `contents` values as a `tuple`.

        Returns:
            A tuple equivalent to `dict.values()`.

        """
        return tuple(self.contents.values())

    """ Dunder Methods """

    def __getitem__(self, key: Hashable) -> Any:
        """Returns value for `key` in `contents`.

        Args:
            key: key in `contents` for which a value is sought.

        Returns:
            Value stored in `contents`.

        """
        return self.contents[key]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Sets `key` in `contents` to `value`.

        Args:
            key: key to set in `contents`.
            value: value to be paired with `key` in `contents`.

        """
        self.contents[key] = value
        return

    def __add__(self, other: Any) -> Manufacturer:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __iadd__(self, other: Any) -> Manufacturer:  # noqa: PYI034
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __delitem__(self, item: Hashable) -> Manufacturer:
        """Deletes `item` from `contents`.

        Args:
            item: item or key to delete in `contents`.

        Raises:
            KeyError: if `item` is not in `contents`.

        """
        self.delete(item = item)
        return self

    def __iter__(self) -> Iterator[Any]:
        """Returns iterator of `contents`.

        Returns:
            Iterator of `contents`.

        """
        return iter(self.contents)

    def __len__(self) -> int:
        """Returns length of `contents`.

        Returns:
            Length of `contents`.

        """
        return len(self.contents)
