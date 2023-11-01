"""Mixins for created object modification.

Contents:
    Classer (`base.Producer`, `abc.ABC`): Producer with an `produce` method that
        always returns a class.
    Flexer (`base.Producer`, `abc.ABC`): Producer that conditions return value
        of the `produce` method based on whether `parameters` are passed.
    Instancer (`base.Producer`, `abc.ABC`): Producer with an `produce` method
        that always returns an instance.

"""
from __future__ import annotations

import abc
import dataclasses
import inspect
from typing import TYPE_CHECKING, Any

from . import base, shared

if TYPE_CHECKING:
    from collections.abc import Hashable, MutableMapping


@dataclasses.dataclass
class Classer(base.Producer, abc.ABC):
    """Producer with an `produce` method always return a class."""

    """ Class Methods """

    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: MutableMapping[Hashable, Any] | None = None,
        **kwargs: Any) -> Any:
        """Modifies `item` and possibly incorporates `parameters`.

        Args:
            item: item created by a constructor that may need to be altered
                before being returned by the constructor `create` method.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`. The argument for `parameters` is ignored by
                `Classer` - it is only included to provide a consistent
                interface across all `Producer` subclasses.
            kwargs: allows subclass to take kwargs.

        Returns:
            Modified item.

        """
        return item if inspect.isclass(item) else item.__class__


@dataclasses.dataclass
class Flexer(base.Producer, abc.ABC):
    """Producer that conditions return value of the `produce` method.

    If `parameters` are passed to the `produce` method, an instance is always
    returned. If no `parameters` are passed, the item will be returned as-is
    (depending on the constructor used).

    """

    """ Class Methods """

    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: MutableMapping[Hashable, Any] | None = None,
        **kwargs: Any) -> Any:
        """Modifies `item` and possibly incorporates `parameters`.

        Args:
            item: item created by a constructor that may need to be altered
                before being returned by the constructor `create` method.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            kwargs: allows subclass to take kwargs.

        Returns:
            Modified item.

        """
        if parameters is None:
            return item
        elif inspect.isclass(item):
            return item(**parameters)
        else:
            return shared.inject_attributes(item, parameters)


@dataclasses.dataclass
class Instancer(base.Producer, abc.ABC):
    """Producer with an `produce` method always return an instance."""

    """ Class Methods """

    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: MutableMapping[Hashable, Any] | None = None,
        **kwargs: Any) -> Any:
        """Modifies `item` and incorporates `parameters`.

        Args:
            item: item created by a constructor that may need to be altered
                before being returned by the constructor `create` method.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.
            kwargs: allows subclass to take kwargs.

        Returns:
            Modified item.

        """
        if inspect.isclass(item) and parameters is None:
            return item()
        elif parameters is None:
            return item
        elif inspect.isclass(item):
            return item(**parameters)
        else:
            return shared.inject_attributes(item, parameters)
