"""Factory classes that utilize explicit or implicit registries.

Contents:
    Registrar (`base.Factory`): builds classes and/or instances from a registry
        stored in the `registry` class attribute.
    AutoRegistrar (`Registrar`, `abc.ABC`): `Registrar` that automatically
        registers its subclasses.
    Subclasser (base.Factory, abc.ABC): builds classes and/or instances from the
        `__subclasses__` method and a dynamically created registry based upon
        it.

"""

from __future__ import annotations

import abc
import copy
import dataclasses
from collections.abc import Hashable, MutableMapping, MutableSequence
from collections.abc import Set as AbstractSet
from typing import Any, ClassVar, Literal, TypeAlias

from . import base, options, shared

GenericDict: TypeAlias = MutableMapping[Hashable, Any]
GenericList: TypeAlias = MutableSequence[Any]
GenericSet: TypeAlias = AbstractSet[Any]
SubsetReturns: TypeAlias = Literal["class", "copy", "simple"]


@dataclasses.dataclass
class Registrar(base.Factory):
    """Builds an item from a registry.

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[base.GenericDict] = {}

    """ Class Methods """

    @classmethod
    def create(
        cls, item: str, parameters: base.GenericDict | None = None
    ) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        Args:
            item (Hashable): name corresponding to a key in `registry`.
            parameters: keyword arguments to pass or add to a created instance.

        Raises:
            KeyError: If a corresponding item in `registry` does not exist for
                `item.`

        Returns:
            Any: created item.

        """
        item = _get_from_registry(item=item, registry=cls.registry)
        return shared.finalize(item=item, parameters=parameters)


@dataclasses.dataclass
class AutoRegistrar(Registrar, abc.ABC):
    """Mixin for core package base classes.

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[base.GenericDict] = {}

    """ Initialization Methods """

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Automatically registers subclasses.

        Each direct subclass of `AutoRegistrar` that does not define its own
        `registry` gets a new one so that unrelated class families do not share
        (and pollute) a single registry. Deeper subclasses register in the
        registry they inherit.

        """
        super().__init_subclass__(**kwargs)
        if cls.registry is AutoRegistrar.registry:
            cls.registry = {}
        cls.registry[options._KEY_NAMER(cls)] = cls


@dataclasses.dataclass
class Subclasser(base.Factory, abc.ABC):
    """Builds a subclass without requiring a storage attribute.

    Unlike some other factories, this one does not require any class attributes.
    Instead, it relies on pre-existing data and lazily adds keys to create
    a registry facade.

    This factory uses the subclasses stored in `__subclasses__` class method
    that is automatically created with every class. It creates a `dict` on the
    fly with key names based on `configuration._KEY_NAMER`. Because of this,
    `Subclasser` should ordinarily be used as a mixin (although it could simply
    be subclassed, if you prefer).

    """

    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Any,
        parameters: base.GenericDict | None = None,
        **kwargs: base.Kwargs,
    ) -> Any:
        """Creates an item based on `item` and possibly `parameters`.

        A subclass in the `__subclasses__` class method is selected based on the
        naming convention in `wonka._KEY_NAMER`.

        Args:
            item: data for construction of the returned item.
            parameters: keyword arguments to pass or add to a created instance.
            kwargs: allows subclass to take kwargs.

        Raises:
            KeyError: If a corresponding subclass does not exist for `item.`

        Returns:
            Any: created item.

        """
        keyer = options._KEY_NAMER
        all_subclasses = _get_all_subclasses(cls)
        registry = {keyer(s): s for s in all_subclasses}
        item = _get_from_registry(item=item, registry=registry)
        return shared.finalize(item=item, parameters=parameters)


def _get_from_registry(item: str, registry: base.GenericDict) -> Any:
    """Returns a copy of a stored item in `registry` with the key of `item`.

    Args:
        item (Hashable): key for item sought in `registry`.
        registry: registry where the sought item is stored.

    Raises:
        KeyError: if `item` does not match any key in `registry`.

    Returns:
        Any: a deep copy of an item stored in `registry`.

    """
    try:
        return copy.deepcopy(registry[item])
    except KeyError as e:
        raise KeyError(f"{item} was not found in the registry") from e


def _get_all_subclasses(item: type[Any]) -> list[type[Any]]:
    """Returns a list of all subclasses of `items`, including indirect ones.

    Args:
        item: class for which to find subclasses.

    Returns:
        List of all subclasses of `item`.

    """
    return list(
        set(item.__subclasses__()).union(
            [s for c in item.__subclasses__() for s in _get_all_subclasses(c)]
        )
    )


# @dataclasses.dataclass
# class Kinds(MutableMapping):
#     """An optional registry for storing and retrieving kinds of objects.

#     A `Kinds` differs from an ordinary python `dict` by including `add` and
#     `subset` methods, storing data in `contents`, and allowing the "+" operator
#     to join `Kinds` instances with other mappings, including `Kinds` instances.

#     In addition, it differs in 2 other significant ways:
#         1) When returning `keys`, `values` and `items`, this class returns them
#             as tuples instead of `KeysView`, `ValuesView`, and `ItemsView`.
#         2) It includes similar functionality to `defaultdict` in the python
#             standard library, including a `setdefault` method. The default is
#             used by the `get` method (not by `[]` access).

#     Args:
#         base: related class for which subclasses are registered.
#         contents: stored dictionary. Defaults to an empty `dict`.
#         default_factory: default value to return or default callable to use to
#             create the default value when `get` is called with a missing key.
#             Defaults to `None`.

#     """

#     base: type | None = dataclasses.field(default = None)
#     contents: GenericDict = dataclasses.field(default_factory=dict)
#     default_factory: Any | None = None

#     """ Class Methods """

#     @classmethod
#     def fromkeys(
#         cls, keys: GenericList, value: Any, **kwargs: Any
#     ) -> Kinds:
#         """Emulates the `fromkeys` class method from a python `dict`.

#         Args:
#             keys: items to be keys in a new `Dictionary`.
#             value: the value to use for all values in a new `Dictionary`.
#             **kwargs: additional arguments to pass to the class constructor (e.g.
#                 `default_factory`).

#         Returns:
#             An instance formed from `keys` and `value`.

#         """
#         return cls(contents=dict.fromkeys(keys, value), **kwargs)

#     """ Instance Methods """

#     def add(self, item: GenericDict, **kwargs: Any) -> None:
#         """Adds `item` to the `contents` attribute.

#         Args:
#             item: items to add to `contents` attribute.
#             **kwargs: additional key/value pairs to add, as in `dict.update`.

#         """
#         self.contents.update(item, **kwargs)

#     def delete(self, item: Hashable) -> None:
#         """Deletes `item` in `contents`.

#         Args:
#             item: key in `contents` to delete the key/value pair.

#         Raises:
#             KeyError: if `item` is not a key in `contents`.

#         """
#         del self.contents[item]

#     def get(self, key: Hashable, default: Any | None = None) -> Any:
#         """Returns value in `contents` or default options.

#         Args:
#             key: key for value in `contents`.
#             default: default value to return if `key` is not found in
#                 `contents`.

#         Raises:
#             KeyError: if `key` is not in `contents` and `default` and the
#                 `default_factory` attribute are both `None`.

#         Returns:
#             Value matching key in `contents` or a default value. If `default` is
#                 `None`, the `default_factory` attribute is used: it is called
#                 if it is callable and returned as is otherwise.

#         """
#         try:
#             return self[key]
#         except (KeyError, TypeError) as error:
#             if default is not None:
#                 return default
#             if self.default_factory is None:
#                 raise KeyError(f"{key} is not in the Dictionary") from error
#             if callable(self.default_factory):
#                 return self.default_factory()
#             return self.default_factory

#     def items(self) -> tuple[tuple[Hashable, Any], ...]:  # type: ignore[override]
#         """Emulates python dict `items` method.

#         Returns:
#             A `tuple` equivalent to `dict.items()`.

#         """
#         return tuple(zip(self.keys(), self.values(), strict=True))

#     def keys(self) -> tuple[Hashable, ...]:  # type: ignore[override]
#         """Returns `contents` keys as a tuple.

#         Returns:
#             A `tuple` equivalent to `dict.keys()`.

#         """
#         return tuple(self.contents.keys())

#     def register(self, item: type, name: str | None = None) -> None:
#         """Registers a new subclass of the base class.

#         Args:
#             item: The subclass to register.
#             name: The name to associate with the subclass. If None, the
#                 snakecase name of `item` will be used.

#         """
#         if name is None:
#             name = utilities._namify(item)
#         self.contents[name] = item

#     def setdefault(self, value: Any) -> None:  # type: ignore[override]
#         """Sets default value to return when `get` method is used.

#         Args:
#             value: default value to return when `get` is called and the
#                 `default` parameter to `get` is None.

#         """
#         self.default_factory = value

#     def subset(
#         self,
#         include: Collection[Any] | Any | None = None,
#         exclude: Collection[Any] | Any | None = None,
#         returns: SubsetReturns | None = None,
#     ) -> Any:
#         """Returns a new instance with a subset of `contents`.

#         This method applies `include` before `exclude` if both are passed. If
#         `include` is None, all existing items will be added to the new subset
#         class instance before `exclude` is applied.

#         Args:
#             include: key(s) to include in the new `Dictionary`. Defaults to
#                 `None`.
#             exclude: key(s) to exclude from the new `Dictionary`. Defaults to
#                 `None`.
#             returns: whether to return a new instance of the `Dictionary`
#                 subclass ("class"), a deep copy of the subclass instance
#                 ("copy") or the simple native Python type ("simple"). Defaults
#                 to `None`, which uses the global setting stored in
#                 `settings._SUBSET_RETURN`.

#         Raises:
#             ValueError: if `include` and `exclude` are both None.
#             KeyError: if a key in `include` is not in `contents`.

#         Returns:
#             `dict`-like object with only keys from `include` and no keys in
#                 `exclude`, in the form dictated by the `returns` argument.

#         """
#         if include is None and exclude is None:
#             raise ValueError("include or exclude must not be None")
#         if include is None:
#             contents = copy.deepcopy(self.contents)
#         else:
#             include = list(utilities._iterify(include))
#             contents = {k: self.contents[k] for k in include}
#         if exclude is not None:
#             exclude = list(utilities._iterify(exclude))
#             contents = {k: v for k, v in contents.items() if k not in exclude}
#         return utilities._return_subset(
#             subset=contents, existing=self, returns=returns
#         )

#     def values(self) -> tuple[Any, ...]:  # type: ignore[override]
#         """Returns `contents` values as a `tuple`.

#         Returns:
#             A `tuple` equivalent to `dict.values()`.

#         """
#         return tuple(self.contents.values())

#     """ Dunder Methods """

#     def __getitem__(self, key: Hashable) -> Any:
#         """Returns value for `key` in `contents`.

#         Args:
#             key: key in `contents` for which a value is sought.

#         Returns:
#             Value stored in `contents`.

#         """
#         return self.contents[key]

#     def __setitem__(self, key: Hashable, value: Any) -> None:
#         """Sets `key` in `contents` to `value`.

#         Args:
#             key: key to set in `contents`.
#             value: value to be paired with `key` in `contents`.

#         """
#         self.contents[key] = value

#     def __add__(self, other: Any) -> Self:
#         """Returns a deep copy with `other` combined using the `add` method.

#         Args:
#             other: item to add to the copy's `contents` using the `add` method.

#         Returns:
#             A new instance. The original instance is not modified.

#         """
#         new_instance = copy.deepcopy(self)
#         new_instance.add(item=other)
#         return new_instance

#     def __iadd__(self, other: Any) -> Self:
#         """Combines argument with `contents` using the `add` method.

#         Args:
#             other: item to add to `contents` using the `add` method.

#         Returns:
#             The instance, modified in place.

#         """
#         self.add(item=other)
#         return self

#     def __delitem__(self, item: Hashable) -> None:
#         """Deletes `item` from `contents`.

#         Args:
#             item: item or key to delete in `contents`.

#         Raises:
#             KeyError: if `item` is not in `contents`.

#         """
#         self.delete(item=item)

#     def __iter__(self) -> Iterator[Any]:
#         """Returns iterator of `contents`.

#         Returns:
#             Iterator of `contents`.

#         """
#         return iter(self.contents)

#     def __len__(self) -> int:
#         """Returns length of `contents`.

#         Returns:
#             Length of `contents`.

#         """
#         return len(self.contents)
