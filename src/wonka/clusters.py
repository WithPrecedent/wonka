"""Stores groups of `wonka` constructors.

Contents:
    Manufacturer: `dict`-like class that stores `wonka` constructors. Has an
        `add` method that validates any added values as `wonka` compatible.

"""
from __future__ import annotations

import abc
import contextlib
import dataclasses
import inspect
from collections.abc import ClassVar, Hashable, MutableMapping
from types import SimpleNamespace
from typing import Any

from . import base, options, registries, shared, utilities


@dataclasses.dataclass
class Manufacturer(base.Cluster):
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

    contents: base.ConstructorDict = dataclasses.field(default_factory = dict)

    """ Instance Methods """

    def add(self, item: base.ConstructorDict | base.Constructor) -> None:
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
            key = options._KEY_NAMER(item)
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
        return tuple(zip(self.keys(), self.values(), strict = True))

    def keys(self) -> tuple[Hashable, ...]:
        """Returns `contents` keys as a `tuple`.

        Returns:
            A `tuple` equivalent to `dict.keys()`.

        """
        return tuple(self.contents.keys())

    # def subset(
    #     self,
    #     include: Hashable | Sequence[Hashable] | None = None,
    #     exclude: Hashable | Sequence[Hashable] | None = None) -> Manufacturer:
    #     """Returns a new instance with a subset of `contents`.

    #     This method applies `include` before `exclude` if both are passed. If
    #     `include` is None, all existing items will be added to the new subset
    #     class instance before `exclude` is applied.

    #     Args:
    #         include: key(s) to include in the new `Manufacturer` instance.
    #         exclude: key(s) to exclude from the new `Manufacturer` instance.

    #     Raises:
    #         ValueError: if `include` and `exclude` are both None.

    #     Returns:
    #         New instance with only keys from `include` and no keys in `exclude`.

    #     """
    #     if include is None and exclude is None:
    #         message = 'either the include or exclude argument must not be None'
    #         raise ValueError(message)
    #     if include is None:
    #         contents = copy.deepcopy(self.contents)
    #     else:
    #         include = list(utilities._iterify(include))
    #         contents = {k: self.contents[k] for k in include}
    #     if exclude is not None:
    #         exclude = list(utilities._iterify(exclude))
    #         contents = {
    #             k: v for k, v in contents.items()
    #             if k not in exclude}
    #     new_dictionary = copy.deepcopy(self)
    #     new_dictionary.contents = contents
    #     return new_dictionary

    def values(self) -> tuple[Any, ...]:
        """Returns `contents` values as a `tuple`.

        Returns:
            A tuple equivalent to `dict.values()`.

        """
        return tuple(self.contents.values())


@dataclasses.dataclass
class Hub(base.Cluster):
    """Stores Keystone classes.

    Attributes:
        contents: dictionary of all direct Keystone
            subclasses. Keys are snakecase names of the Keystone subclass and
            values are the base Keystone subclasses.
        defaults: dictionary of the default class
            for each of the Keystone subclasses. Keys are snakecase names of the
            base type and values are Keystone subclasses.
        All direct Keystone subclasses will have an attribute name added
        dynamically.

    """
    contents: base.ConstructorDict = dataclasses.field(default_factory = dict)
    defaults: base.GenericDict = dataclasses.field(default_factory = dict)

    """ Properties """

    @property
    def registry(self) -> SimpleNamespace:
        """Returns an object of `contents` supporting dot access."""
        return SimpleNamespace(self.contents)

    """ Public Methods """

    @classmethod
    def add(cls, item: type[Keystone]) -> None:
        """Adds a new keystone attribute with an empty dictionary.

        Args:
            item: direct Keystone subclass from which the name
                of a new attribute should be derived.

        """
        name = cls._get_name(item = item)
        cls.bases[name] = item
        setattr(cls, name, cls.default_factory())
        # Automatically sets cls to the default option if it is concrete.
        if abc.ABC not in item.__bases__:
            cls.set_default(item = item, base = name)
        # Otherwise the default is set to None (if there is no previously
        # assigned default option).
        elif name not in cls.defaults:
            cls.defaults[name] = None
        return

    @classmethod
    def classify(cls, item: str | type[Keystone] | Keystone) -> str:
        """Returns the str name of the Keystone of which `item` is.

        Args:
            item: Keystone subclass, subclass instance, or its str name.

        Raises:
            ValueError: if `item` does not match a subclass of any Keystone
                type.

        Returns:
            str: snakecase str name of the Keystone base type of which `item` is
                a subclass or subclass instance.

        """
        if isinstance(item, str):
            for key in cls.bases:
                subtype_library = getattr(cls, key)
                for name in subtype_library:
                    if item == name:
                        return key
        else:
            if not inspect.isclass(item):
                item = item.__class__
            for key, value in cls.bases.items():
                if issubclass(item, value):
                    return key
        raise ValueError(f'{item} is not a subclass of any Keystone')

    @classmethod
    def register(
        cls,
        item: type[Keystone],
        name: str | None = None,
        base: str | None = None) -> None:
        """Registers `item` in the appropriate class attribute registry.

        Args:
            item: Keystone subclass to register.
            name: key name to use in storing `item`. Defaults to None.
            base: class to use for the newly created insance. Defaults to None.

        """
        name = name or cls._get_name(item = item, name = name)
        keystone = cls.classify(item)
        getattr(cls, keystone)[name] = item
        if cls.defaults[keystone] is None and abc.ABC not in item.__bases__:
            cls.set_default(item = item, base = keystone)
        return

    @classmethod
    def set_default(
        cls,
        item: type[Keystone],
        name: str | None = None,
        base: str | None = None) -> None:
        """Registers `item` as the default subclass of 'base'.

        If 'base' is not passed, the 'classify' method will be used to determine
        the appropriate base.

        Args:
            item (Type[Keystone]): Keystone subclass to make the default.
            name (Optional[str], optional): key name to use in the 'defaults'
                dictionary. Defaults to None.
            base (Optional[str]): key name to use in storing `item`. Defaults to
                None.

        """
        key = base or cls.classify(item)
        name = cls._get_name(item = item, name = name)
        cls.defaults[key] = name
        return

    @classmethod
    def validate(
        cls,
        item: object,
        attribute: str,
        parameters: base.GenericDict | None = None) -> object:
        """Creates or validates 'attribute' in `item`.

        Args:
            item: object (often a Project or Manager instance) of which
                a Keystone in 'attribute' needs to be validated or
                created.
            attribute: name of the attribute' in item containing a value
                to be validated or which provides information to create an
                appropriate instance.
            parameters: parameters to pass
                to or inject in the Keystone subclass instance.

        Raises:
            ValueError: if the value of 'attribute' in `item` does match any
                known subclass or subclass instance of that Keystone
                subtype.

        Returns:
            Completed, linked instance.

        """
        parameters = parameters or {}
        instance = None
        # Get current value of 'attribute' in `item`.
        value = getattr(item, attribute)
        # Get the corresponding base class.
        base = cls.bases[attribute]
        # Gets the relevant registry for 'attribute'.
        registry = getattr(cls, attribute)
        # Adds parameters to 'value' is already an instance of the appropriate
        # base type.
        if isinstance(value, base):
            for parameter, argument in parameters.items():
                setattr(value, parameter, argument)
            instance = value
        # Selects default class for 'attribute' if none exists.
        elif value is None:
            name = cls.defaults[attribute]
            if name:
                value = registry[name]
            else:
                raise ValueError(
                    f'Neither a value for {attribute} nor a default class '
                    f'exists')
        # Uses str value to select appropriate subclass.
        elif isinstance(value, str):
            name = getattr(item, attribute)
            value = registry[name]
        # Gets name of class if it is already an appropriate subclass.
        elif inspect.issubclass(value, base):
            name = utilities._namify(value)
        else:
            raise ValueError(f'{value} is not a recognized keystone')
        # Creates a subclass instance.
        if instance is None:
            instance = value.create(name = name, **parameters)
        setattr(item, attribute, instance)
        return item

    """ Private Methods """

    @classmethod
    def _get_name(
        cls,
        item: type[Keystone],
        name: str | None = None) -> None:
        """Returns 'name' or str name of item.

        By default, the method uses utilities._namify to create a snakecase
        name. If the resultant name begins with 'project_', that substring is
        removed.

        If you want to use another naming convention, just subclass and override
        this method. All other methods will call this method for naming.

        Args:
            item: item to name.
            name: optional name to use. A 'project_'
                prefix will be removed, if it exists. Defaults to None.

        Returns:
            str: name of `item` or 'name' (with the 'project' prefix removed).

        """
        name = name or utilities._namify(item)
        if name.startswith('project_'):
            name = name[8:]
        return name


@dataclasses.dataclass
class Keystone(registries.AutoRegistrar):
    """_summary

    Attributes:
        registry: stores classes and/or instances to be used in item
            construction. Defaults to an empty `dict`.

    """

    registry: ClassVar[base.GenericDict] = {}  # noqa: RUF008
    hub: ClassVar[Hub] = Hub

    """ Initialization Methods """

    @classmethod
    def __init_subclass__(cls, *args: Any, **kwargs: Any):
        """Automatically registers subclasses."""
        with contextlib.suppress(AttributeError):
            super().__init_subclass__(*args, **kwargs)
        keyer = options._KEY_NAMER
        key = keyer(cls)
        cls.registry[key] = cls
