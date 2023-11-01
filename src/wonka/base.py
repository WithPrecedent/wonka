"""Base classes for `wonka` constructors.

Contents:
    Factory (`abc.ABC`): interface for basic `wonka` creation classes. A
        `create` class method is required for subclasses.
    Manager (`Iterable`, `abc.ABC`): iterable interface for complex construction
        managers. A `manage` instance method is required for subclasses. For
        compatibility as a `wonka` constructor, a `create` property is included
        which automatically calls the `manage` method with all args and kwargs.
    Producer (`abc.ABC`): mixin interface for classes that alter created items
        before returning them. A `produce` class method is required for
        subclasses.
    Constructor (`TypeAlias`): type alias for a wonka-compatible constructor
        type. By default, it includes a `Factory` subclass, a `Factory` subclass
        instance, and a `Manager` subclass instance.

"""

from __future__ import annotations

import abc
import dataclasses
from collections.abc import Hashable, Iterable, Iterator, MutableMapping
from typing import Any, TypeAlias


@dataclasses.dataclass
class Factory(abc.ABC):
    """Base for `wonka` constructors.

    A `wonka` `Factory` can be subclassed into any constructer design (not just
    those that fit the classical factory design pattern). So, for example, the
    `wonka` package itself includes `Factory` subclasses that fit the prototype
    (`Scribe`), registry (`Registar` and` Subclasser`), and traditional
    (`Delegate` and `Sourcerer`) design patterns. Further, a `Manager` class
    instance may act as the director in a builder design pattern.

    One of the goals of `wonka`, though, is not be be wedded to or worried about
    the underlying design pattern. Instead, all constructers follow the simple,
    universal, and easily extensible interface of `Factory`.

    If you want to add code that modifies output of a `Factory`'s `create` class
    method, you can either include that in the subclass `create` method or by
    mixing in a `Producer` class. Details on how to use `Producer` subclasses
    are included in its documentation.

    """

    """ Required Subclass Methods """

    @classmethod
    @abc.abstractmethod
    def create(cls, item: Any, *args: Any, **kwargs: Any) -> Any:
        """Returns a created or modified item.

        Args:
            item: data for creation of an item or an item to be modified.
            args: allows subclass to take args.
            kwargs: allows subclass to take kwargs.

        Returns:
            Any: created or modified item.

        """


@dataclasses.dataclass
class Manager(Iterable, abc.ABC):
    """Base for manageing complex class or object construction.

    Args:
        contents: an iterable containing `Factory` subclasses or `Manager`
            subclass instances.

    """

    contents: Iterable

    """ Required Subclass Methods """

    @abc.abstractmethod
    def manage(self, item: Any, *args: Any, **kwargs: Any) -> Any:
        """Manages construction and/or modification based on `item`.

        Args:
            item: item to be passed to factories in `contents`.
            args: allows subclass to take args.
            kwargs: allows subclass to take kwargs.

        Returns:
            Any: constructed item.

        """

    """ Properties """

    @property
    def create(self, *args: Any, **kwargs:  Any) -> Any:
        """Calls `manage` method with args and kwargs.

        This property is included as a convenience so that an instance of a
        `Manager` can be used as a drop-in for a `Factory` subclass. `Manager`
        cannot easily be made a subclass for `Factory` because it will often
        need to rely on instance data for construction. So, every `Manager`
        subclass should be designed such that an instance of that subclass could
        be substituted for a `Factory` subclass. This allows other `Manager`
        subclass instances to be stored in `contents` as part of an iterable
        workflow.

        """
        return self.manage(*args, **kwargs)

    """ Dunder Methods """

    def __iter__(self) -> Iterator:
        """Returns iterable of `contents`.

        `Manager` is agnostic as to the type of iterable that is used in order
        to accomodate simple sequences, complex graphs, nested trees, or any
        other workflow design. As a general practice, though, any mapping should
        probably return `items()` so that the interface for iteration never
        requires any appended method call. But nothing in `wonka` precludes a
        different rule or practice.

        """
        return iter(self.contents)


@dataclasses.dataclass
class Producer(abc.ABC):
    """Base mixin for modifying items.

    A `Producer`'s `produce` method will automatically be called if it is
    mixed-in with any of the `Factory` classes in `wonka`. If you want a custom
    `Factory` subclass to similarly automatically check for a `produce` method,
    the easiest way to do that is to simply call the `finalize` function as your
    return value for the `Factory`'s `create` method as follows:

    ```python
    return wonka.finalize(item = item, parameters = parameters)
    ```
    """

    """ Required Subclass Methods """

    @classmethod
    @abc.abstractmethod
    def produce(
        cls,
        item: Any,
        parameters: MutableMapping[Hashable, Any] | None = None) -> Any:
        """Modifies `item` and possibly incorporates `parameters`.

        Args:
            item: item to be modified.
            parameters: keyword arguments to pass or add to a created instance.
                Defaults to `None`.

        Returns:
            Any: modified item.

        """


Constructor: TypeAlias = Factory | type[Factory] | Manager
