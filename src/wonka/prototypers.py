"""Factory classes that clone items.

Contents:
    Scribe (`base.Factory`): factory that clones a passed argument or, if none
        is passed, itself.

"""
from __future__ import annotations

import copy
import dataclasses
from typing import Any

from . import base, shared


@dataclasses.dataclass
class Scribe(base.Factory):
    """Base class for cloning classes or objects."""

    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Any | None = None,
        parameters: base.GenericDict | None = None,
        **kwargs: base.Kwargs) -> Any:
        """Clones `item` and possibly incorporates `parameters`.

        Args:
            item: item to clone. If it is None, the `create` method assumes that
                it should clone itself. Defaults to None.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            kwargs: allows subclass to take kwargs.

        Returns:
            Cloned item.

        """
        item = item or cls
        item = copy.deepcopy(item)
        return shared.finalize(item = item, parameters = parameters)
