"""Manager classes for iterable constructors.

Contents:
    Assembler (`MutableSequence`, `base.Manager`): iterable that stores a list
        of constructors that build an item like an assembly line.

"""

from __future__ import annotations

import copy
import dataclasses
from collections.abc import Iterable, Iterator, MutableSequence, Sequence
from typing import Any, Self, overload

from . import base, shared, utilities


@dataclasses.dataclass
class Assembler(MutableSequence[base.Constructor], base.Manager):
    """Assembly line constructor.

    Assembler stores a sequence of wonka constructors that are called by the
    `manage` (or `create`) method in order to construct an item.

    Args:
        contents: stored constructors. Defaults to an empty list.

    """

    contents: MutableSequence[base.Constructor] = dataclasses.field(
        default_factory = list)

    """ Public Methods """

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
        elif (
                isinstance(item, Sequence)
                and all(shared.is_constructor(v) for v in item)):
            self.contents.extend(item)
        else:
            message = 'All values in item must be wonka-compatible constructors'
            raise TypeError(message)

    def delete(self, item: int | slice) -> None:
        """Deletes item(s) at the index or slice in `contents`.

        Args:
            item: index or slice in `contents` to delete.

        Raises:
            IndexError: if `item` is an index that is not in `contents`.

        """
        del self.contents[item]

    def insert(self, index: int, value: base.Constructor) -> None:
        """Inserts `value` at `index` in `contents`.

        `MutableSequence` uses this method for `append`, `extend`, and `+=`, so
        those methods are validated too.

        Args:
            index: index to insert `value` at.
            value: constructor to be inserted.

        """
        _validate_constructors([value])
        self.contents.insert(index, value)

    def manage(self, item: Any, **kwargs: base.Kwargs) -> Any:
        """Manages construction and/or modification based on `item`.

        Args:
            item: item to be passed to constructors in `contents`.
            **kwargs: keyword arguments passed to each constructor.

        Returns:
            Constructed item.

        """
        for constructor in self.contents:
            item = constructor.create(item, **kwargs)
        return item

    def prepend(
            self,
            item: base.Constructor | Sequence[base.Constructor]) -> None:
        """Prepends `item` to `contents`.

        If `item` is a sequence of constructors (and not a constructor itself,
        such as an `Assembler`), `prepend` adds its contents to the stored list
        in the order they appear in `item`.

        Args:
            item: item(s) to prepend to `contents`.

        Raises:
            TypeError: if all of the values of `item` are not wonka-compatible
                constructors.

        """
        if shared.is_constructor(item):
            self.insert(0, item)
        elif isinstance(item, Sequence) and not isinstance(item, str):
            _validate_constructors(item)
            self.contents[0:0] = list(item)
        else:
            message = 'All values in item must be wonka-compatible constructors'
            raise TypeError(message)

    def subset(
            self,
            include: Any | Sequence[Any] | None = None,
            exclude: Any | Sequence[Any] | None = None) -> Self:
        """Returns a new instance with a subset of `contents`.

        This method applies `include` before `exclude` if both are passed. If
        `include` is `None`, all existing items will be added to the new subset
        class instance before `exclude` is applied.

        Args:
            include: item(s) to include in the new instance. Defaults to `None`.
            exclude: item(s) to exclude in the new instance. Defaults to `None`.

        Raises:
            ValueError: if `include` and `exclude` are both `None`.

        Returns:
            Assembler with only items from `include` and no items in `exclude`.

        """
        if include is None and exclude is None:
            message = 'include or exclude must not be None'
            raise ValueError(message)
        contents = list(self.contents)
        if include is not None:
            included = list(utilities._iterify(include))
            contents = [i for i in contents if i in included]
        if exclude is not None:
            excluded = list(utilities._iterify(exclude))
            contents = [i for i in contents if i not in excluded]
        new_assembler = copy.copy(self)
        new_assembler.contents = copy.deepcopy(contents)
        return new_assembler

    """ Dunder Methods """

    @overload
    def __getitem__(self, index: int) -> base.Constructor: ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[base.Constructor]:
        ...

    def __getitem__(
            self,
            index: int | slice) -> (
                base.Constructor | MutableSequence[base.Constructor]):
        """Returns value(s) for `index` in `contents`.

        Args:
            index: index or slice to search for in `contents`.

        Returns:
            Item stored in `contents` at `index` or the items in the slice.

        """
        return self.contents[index]

    @overload
    def __setitem__(self, index: int, value: base.Constructor) -> None: ...

    @overload
    def __setitem__(
            self,
            index: slice,
            value: Iterable[base.Constructor]) -> None: ...

    def __setitem__(
            self,
            index: int | slice,
            value: base.Constructor | Iterable[base.Constructor]) -> None:
        """Sets `index` in `contents` to `value`.

        Args:
            index: index or slice to set `value` to in `contents`.
            value: constructor (or, for a slice, constructors) to be set at
                `index` in `contents`.

        """
        if isinstance(index, slice):
            values = list(value)  # type: ignore[arg-type]
            _validate_constructors(values)
            self.contents[index] = values
        else:
            _validate_constructors([value])
            self.contents[index] = value  # type: ignore[assignment]

    def __add__(
            self,
            other: base.Constructor | Sequence[base.Constructor]) -> Self:
        """Returns a deep copy with `other` combined using the `add` method.

        Args:
            other: item to add to the copy's `contents` using the `add` method.

        Returns:
            A new instance. The original instance is not modified.

        """
        new_assembler = copy.deepcopy(self)
        new_assembler.add(item = other)
        return new_assembler

    def __iadd__(  # type: ignore[override]
            self,
            other: base.Constructor | Sequence[base.Constructor]) -> Self:
        """Combines argument with `contents` using the `add` method.

        Args:
            other: item to add to `contents` using the `add` method.

        Returns:
            The instance, modified in place.

        """
        self.add(item = other)
        return self

    def __delitem__(self, index: int | slice) -> None:
        """Deletes item(s) at `index` in `contents`.

        Args:
            index: index or slice of item(s) to delete in `contents`.

        """
        self.delete(item = index)

    def __iter__(self) -> Iterator[base.Constructor]:
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


""" Private Functions """


def _validate_constructors(items: Iterable[Any]) -> None:
    """Raises an error if any of `items` is not a wonka-compatible constructor.

    Args:
        items: items to validate.

    Raises:
        TypeError: if any of `items` is not a wonka-compatible constructor.

    """
    if not all(shared.is_constructor(i) for i in items):
        message = 'All values in item must be wonka-compatible constructors'
        raise TypeError(message)
