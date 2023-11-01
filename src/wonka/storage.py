"""Stores groups of wonka constructors.

Contents:
    Manufacturer (camina.Dictionary): dict-like class that stores wonka
        constructors. Has an 'add' method while validates any added values as
        wonka compatible.

"""
from __future__ import annotations

import copy
import dataclasses
from collections.abc import Hashable, Iterator, MutableMapping, Sequence
from typing import Any, Self

from . import base, configuration, shared, utilities


@dataclasses.dataclass
class Manufacturer(MutableMapping):
    """Dictionary of factories.

    A Manufacturer may serve as a one-stop spot for constructors. Each
    constructor need not be of the same subtype, as they pass the
    'is_constructor' test. The use of a Manufacturer is wholly optional - it is
    just a convenience offered by wonka. To access individual constructors, the
    following format should be used:

    manufacturer_instance['constructor_name'].create(*args, **kwargs)


    Args:
        contents (MutableMapping[Hashable, base.Constructor]): stored dict of
            wonka constructors. Defaults to an empty dict.
        default_factory (Optional[Any]): default value to return or default
            callable to use to create the default value.

    """

    contents: MutableMapping[Hashable, base.Constructor] = dataclasses.field(
        default_factory = dict)
    default_factory: Any | None = None

    """ Class Methods """

    @classmethod
    def fromkeys(
        cls,
        keys: Sequence[Hashable],
        value: Any,
        **kwargs: Any) -> Manufacturer:
        """Emulates the 'fromkeys' class method from a python dict.

        Args:
            keys (Sequence[Hashable]): items to be keys in a new Dictionary.
            value (Any): the value to use for all values in a new Dictionary.

        Returns:
            Dictionary: formed from 'keys' and 'value'.

        """
        return cls(contents = dict.fromkeys(keys, value), **kwargs)

    """ Instance Methods """

    def add(
        self,
        item: MutableMapping[
            Hashable, base.Constructor] | base.Constructor) -> None:
        """Adds 'item' to the 'contents' attribute.

        Args:
            item (MutableMapping[Hashable, Any] | base.Constructor): item(s) to
                add to 'contents' attribute.


        Raises:
            TypeError: if all of the values of 'item' are not wonka-compatible
                constructors or if 'item' itself is not a wonka-compatible
                constructor.

        """
        if isinstance(item, MutableMapping):
            if all(shared.is_constructor(v) for v in item.values()):
                self.contents.update(item)
            else:
                raise TypeError(
                    'All values in item must be wonka-compatible constructors')
        elif shared.is_constructor(item):
            key = configuration._KEY_NAMER(item)
            self.contents.update({key: item})
        else:
            raise TypeError(
                'item must either be a wonka-compatible constructor or a dict-'
                'like object with values that are constructors')

    def delete(self, item: Hashable) -> None:
        """Deletes 'item' in 'contents'.

        Args:
            item (Hashable): key in 'contents' to delete the key/value pair.

        """
        del self.contents[item]
        return

    def get(self, key: Hashable, default: Any | None = None) -> Any:
        """Returns value in 'contents' or default options.

        Args:
            key (Hashable): key for value in 'contents'.
            default (Optional[Any]): default value to return if 'key' is not
                found in 'contents'.

        Raises:
            KeyError: if 'key' is not in the Dictionary and 'default' and the
                'default_factory' attribute are both None.

        Returns:
            Any: value matching key in 'contents' or 'default_factory' value.

        """
        try:
            return self[key]
        except (KeyError, TypeError):
            if default is None:
                if self.default_factory is None:
                    raise KeyError(f'{key} is not in the Dictionary')
                else:
                    try:
                        return self.default_factory()
                    except TypeError:
                        return self.default_factory
            else:
                return default

    def items(self) -> tuple[tuple[Hashable, Any], ...]:
        """Emulates python dict 'items' method.

        Returns:
            tuple[tuple[Hashable], Any]: a tuple equivalent to dict.items().

        """
        return tuple(zip(self.keys(), self.values()))

    def keys(self) -> tuple[Hashable, ...]:
        """Returns 'contents' keys as a tuple.

        Returns:
            tuple[Hashable, ...]: a tuple equivalent to dict.keys().

        """
        return tuple(self.contents.keys())

    def setdefault(self, value: Any) -> None:
        """Sets default value to return when 'get' method is used.

        Args:
            value (Any): default value to return when 'get' is called and the
                'default' parameter to 'get' is None.

        """
        self.default_factory = value
        return

    def subset(
        self,
        include: Hashable | Sequence[Hashable] | None = None,
        exclude: Hashable | Sequence[Hashable] | None = None) -> Manufacturer:
        """Returns a new instance with a subset of 'contents'.

        This method applies 'include' before 'exclude' if both are passed. If
        'include' is None, all existing items will be added to the new subset
        class instance before 'exclude' is applied.

        Args:
            include (Optional[Hashable | Sequence[Hashable]]): key(s) to
                include in the new Dictionary instance.
            exclude (Optional[Hashable | Sequence[Hashable]]): key(s) to
                exclude from the new Dictionary instance.

        Raises:
            ValueError: if 'include' and 'exclude' are both None.

        Returns:
            Dictionary: with only keys from 'include' and no keys in 'exclude'.

        """
        if include is None and exclude is None:
            raise ValueError('include or exclude must not be None')
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
        """Returns 'contents' values as a tuple.

        Returns:
            tuple[Any, ...]: a tuple equivalent to dict.values().

        """
        return tuple(self.contents.values())

    """ Dunder Methods """

    def __getitem__(self, key: Hashable) -> Any:
        """Returns value for 'key' in 'contents'.

        Args:
            key (Hashable): key in 'contents' for which a value is sought.

        Returns:
            Any: value stored in 'contents'.

        """
        return self.contents[key]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Sets 'key' in 'contents' to 'value'.

        Args:
            key (Hashable): key to set in 'contents'.
            value (Any): value to be paired with 'key' in 'contents'.

        """
        self.contents[key] = value
        return

    def __add__(self, other: Any) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __iadd__(self, other: Any) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __delitem__(self, item: Hashable) -> Self:
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
            Iterator: of `contents`.

        """
        return iter(self.contents)

    def __len__(self) -> int:
        """Returns length of `contents`.

        Returns:
            int: length of `contents`.

        """
        return len(self.contents)
