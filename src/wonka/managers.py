"""Manager classes for iterable constructors.

Contents:
    Assembler (`MutableSequence`, `base.Manager`): iterable that stores a list
        of constructors that build an item like an assembly line.

"""
from __future__ import annotations

import copy
import dataclasses
from collections.abc import Iterator, MutableSequence, Sequence
from typing import Any

from wonka import utilities

from . import base, shared


@dataclasses.dataclass
class Assembler(MutableSequence, base.Manager):
    """Assembly line constructer.

    Assembler stores a sequence of wonka constructors that are called by the
    `manage` (or `create`) method in order to construct an item.

    Args:
        contents: stored constructors. Defaults to an empty list.

    """

    contents: MutableSequence[base.Constructor] = dataclasses.field(
        default_factory = list)

    """ Instance Methods """

    def add(self, item: base.Constructor | Sequence[base.Constructor]) -> None:
        """Adds `item` to the `contents` attribute.

        Args:
            item: item(s) to add to `contents` attribute.


        Raises:
            TypeError: if all of the values of `item` are not wonka-compatible
                constructors.

        """
        if shared.is_constructor(item):
            self.contents.append(item)
        elif (isinstance(item, Sequence)
                and all(shared.is_constructor(v) for v in item)):
            self.contents.extend(item)
        else:
            raise TypeError(
                'All values in item must be wonka-compatible constructors')

    def delete(self, item: int) -> None:
        """Deletes item at the index in `contents`.

        Args:
            item: index in `contents` to delete.

        """
        del self.contents[item]
        return

    def insert(self, index: int, item: Any) -> None:
        """Inserts `item` at `index` in `contents`.

        Args:
            index: index to insert `item` at.
            item: object to be inserted.

        """
        self.contents.insert(index, item)
        return

    def manage(self, item: Any) -> Any:
        """Manages construction and/or modification based on `item`.

        Args:
            item: item to be passed to constructors in `contents`.

        Returns:
            Constructed item.

        """
        for constructor in self.contents:
            item = constructor.create(item)
        return item

    def prepend(self, item: Any | Sequence[Any]) -> None:
        """Prepends `item` to `contents`.

        If `item` is a non-`str` sequence, `prepend` adds its contents to the
        stored list in the order they appear in `item`.

        Args:
            item: item(s) to prepend to `contents`.

        """
        if utilities._is_sequence(item = item):
            for thing in reversed(item):
                self.prepend(item = thing)
        else:
            self.insert(0, item)
        return

    def subset(
        self,
        include: Any | Sequence[Any] | None = None,
        exclude: Any | Sequence[Any] | None = None) -> Assembler:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is None, all existing items will be added to the new subset
        class instance before `exclude` is applied.

        Args:
            include: item(s) to include in the new instance. Defaults to None.
            exclude: item(s) to exclude in the new instance. Defaults to None.

        Raises:
            ValueError: if `include` and `exclude` are both None.

        Returns:
            Assembler with only items from `include` and no items in `exclude`.

        """
        if include is None and exclude is None:
            raise ValueError('include or exclude must not be None')
        else:
            if include is None:
                contents = copy.deepcopy(self.contents)
            else:
                include = list(utilities._iterify(include))
                contents = [i for i in self.contents if i in include]
            if exclude is not None:
                exclude = list(utilities._iterify(exclude))
                contents = [i for i in contents if i not in exclude]
            new_listing = copy.deepcopy(self)
            new_listing.contents = contents
        return new_listing

    """ Dunder Methods """

    def __getitem__(self, index: int) -> base.Constructor:
        """Returns value(s) for `key` in `contents`.

        Args:
            index: index to search for in `contents`.

        Returns:
            Item stored in `contents` at key.

        """
        return self.contents[index]

    def __setitem__(self, index: int, value: base.Constructor) -> None:
        """Sets `key` in `contents` to `value`.

        Args:
            index: index to set `value` to in `contents`.
            value: value to be set at `key` in `contents`.

        """
        self.contents[index] = value
        return

    def __add__(
        self,
        other: base.Constructor | Sequence[base.Constructor]) -> Assembler:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: tem to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __iadd__(  # noqa: PYI034
        self,
        other: base.Constructor | Sequence[base.Constructor]) -> Assembler:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        """
        self.add(item = other)
        return self

    def __delitem__(self, item: int) -> Assembler:
        """Deletes `item` from `contents`.

        Args:
            item: index of item to delete in `contents`.

        Raises:
            KeyError: if `item` is not in `contents`.

        """
        self.delete(item = item)
        return self

    def __iter__(self) -> Iterator[base.Constructor]:
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
