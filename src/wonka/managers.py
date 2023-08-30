"""Manager classes for iterable constructors.

Contents:
    Assembler (camina.Listing, base.Manager): iterable that stores a list of
        constructors that build an item like an assembly line.

"""
from __future__ import annotations

import dataclasses
from collections.abc import MutableSequence, Sequence
from typing import Any

import camina

from . import base, shared


@dataclasses.dataclass
class Assembler(camina.Listing, base.Manager):
    """Assembly line constructer.

    Assembler stores a sequence of wonka constructors that are called by the
    'manage' (or 'create') method in order to construct an item.


    Args:
        contents (MutableMapping[Hashable, base.Factory]): stored constructors.
            Defaults to an empty list.

    """

    contents: MutableSequence[base.Constructor] = dataclasses.field(
        default_factory = list)

    """ Instance Methods """

    def add(self, item: base.Constructor | Sequence[base.Constructor]) -> None:
        """Adds 'item' to the 'contents' attribute.

        Args:
            item (base.Constructor | Sequence[base.Constructor]): item(s) to add
                to 'contents' attribute.


        Raises:
            TypeError: if all of the values of 'item' are not wonka-compatible
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

    def manage(self, item: Any) -> Any:
        """Manages construction and/or modification based on 'item'.

        Args:
            item: item to be passed to constructors in 'contents'.


        Returns:
            Any: constructed item.

        """
        for constructor in self.contents:
            item = constructor.create(item)
        return item
