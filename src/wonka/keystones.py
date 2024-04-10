# """Tools to store subclasses and/or instances.

# Contents:
#     Anthology (base.Registry, camina.Dictionary): registry that stores classes
#         or instances.
#     Corpus (base.Registry, camina.ChainDictionary): registry that stores classes
#         and instances.
#     Library (Anthology): base class for storing base subclasses and/or subclass
#         instances.
#     Librarian (Anthology, camina.ChainDictionary): stores base classes,
#         defaults, and subclasses for project keystones.

# To Do:
#     Add decorators for each registry type (using the commented out code as a
#         template)

# """
# from __future__ import annotations

# import contextlib
# import copy
# import dataclasses

# # import functools
# import inspect
# from typing import TYPE_CHECKING, Any, ClassVar, Optional

# import camina

# from . import base, setup

# if TYPE_CHECKING:
#     from collections.abc import (
#         Hashable,
#         Iterator,
#         MutableMapping,
#         MutableSequence,
#     )


# @dataclasses.dataclass
# class Anthology(base.Registry, camina.Dictionary):
#     """Stores registered instances or classes.

#     Args:
#         contents (MutableMapping[Hashable, Any]): stored dictionary. Defaults
#             to an empty dict.
#         default_factory (Optional[Any]): default value to return or default
#             callable to use to create the default value. Defaults to None.

#     """

#     contents: MutableMapping[Hashable, Any] = dataclasses.field(
#         default_factory = dict)
#     default_factory: Any | None = None

#     """ Instance Methods """

#     def deposit(
#         self,
#         item: object | type[Any],
#         name: Hashable | None = None) -> None:
#         """Adds 'item' to 'contents'.

#         Args:
#             item (object | type[Any]): class or instance to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using 'configuration.KEYER'.
#                 Defaults to None.

#         """
#         name = name or setup.KEYER(item)
#         self.contents[name] = item
#         return

#     def withdraw(self, item: Hashable) -> object | type[Any]:
#         """Returns an instance or class based on 'item'.

#         Args:
#             item (Hashable): key name corresponding to the stored item sought.

#         Returns:
#             object | type[Any]: instance or class from stored items.

#         """
#         try:
#             return self.contents[item]
#         except (KeyError, TypeError):
#             if self.default_factory is None:
#                 raise KeyError(f'{item} is not in the registry')
#             try:
#                 return self.default_factory()
#             except TypeError:
#                 return self.default_factory


# @dataclasses.dataclass
# class Corpus(base.Registry, camina.ChainDictionary):
#     """Stores class instances and classes in a chained mapping.

#     When searching for matches, instances are prioritized over classes.

#     The class should limit the number of chained Anthology instances to 2.
#     Instances are stored in the first slot of 'contents'. And, classes are
#     stored in the second.

#     Args:
#         contents (MutableSequence[MutableMapping[Hashable, Any]]): list of
#             stored Anthology instances. This is equivalent to the 'maps'
#             attribute of a collections.ChainMap instance but uses a different
#             name for compatibility with other mappings in Ashford. A separate
#             'maps' property is included which points to 'contents' to ensure
#             compatibility in the opposite direction.
#         default_factory (Optional[Any]): default value to return or default
#             callable to use to create the default value.
#         return_first (Optional[bool]): whether to only return the first match
#             found (True) or to search all of the stored Anthology instances
#             (False). Defaults to True.
#         storage (Optional[type[Anthology]]): the class to use for each registry
#             stored in 'contents'.

#     """

#     contents: MutableSequence[MutableMapping[Hashable, Any]] = (
#         dataclasses.field(default_factory = list))
#     default_factory: Optional[Any] = None
#     return_first: Optional[bool] = True
#     storage: Optional[type[MutableMapping]] = Anthology

#     """ Initialization Methods """

#     def __post_init__(self) -> None:
#         """Automatically initializes 'contents' attribute."""
#         with contextlib.suppress(AttributeError):
#             super().__post_init__()
#         if not self.contents:
#             self.contents.append(self.storage())
#             self.contents.append(self.storage())

#     """ Properties """

#     @property
#     def instances(self) -> Anthology:
#         """Returns stored instances.

#         Returns:
#             Anthology: with stored instances.

#         """
#         return self.contents[0]

#     @property
#     def classes(self) -> Anthology:
#         """Returns stored classes.

#         Returns:
#             Anthology: with stored classes.

#         """
#         return self.contents[1]

#     """ Instance Methods """

#     def deposit(
#         self,
#         item: object | type[Any],
#         name: Optional[Hashable] = None) -> None:
#         """Adds 'item' to 'contents'.

#         If 'item' is a class, it will be registered in the 'classes'
#         registry. If 'item' is an instance, it will be registered in the
#         'instances' registry and its class will be registered in the
#         'classes' registry. However, if an instance is passed with a 'name'
#         argument, the 'name' will only be used for storing 'item' in the
#         'instances' registry (and the key name will be inferred for the
#         'classes' registry).

#         Args:
#             item (object | type[Any]): subclass or instance to add to the
#                 registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using 'configuration.KEYER'.
#                 Defaults to None

#         """
#         if inspect.isclass(item):
#             self.deposit_subclass(item = item, name = name)
#         else:
#             self.deposit_instance(item = item, name = name)
#             self.deposit_subclass(item = item.__class__)
#         return

#     def deposit_instance(
#         self,
#         item: object,
#         name: Optional[Hashable] = None) -> None:
#         """Adds 'item' to 'contents'.

#         Args:
#             item (object): instance to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using 'configuration.KEYER'.
#                 Defaults to None

#         """
#         name = name or setup.KEYER(item)
#         self.instances[name] = item
#         return

#     def deposit_subclass(
#         self,
#         item: type[Any],
#         name: Optional[Hashable] = None) -> None:
#         """Adds 'item' to 'contents'.

#         Args:
#             item (type[Any]): subclass to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using 'configuration.KEYER'.
#                 Defaults to None

#         """
#         name = name or setup.KEYER(item)
#         self.classes[name] = item
#         return

#     def withdraw(self, item: Hashable) -> type[Any]:
#         """Returns subclass from 'contents'.

#         Args:
#             item (Hashable): key name corresponding to the stored item sought.

#         Returns:
#             type[Any]: subclass matching 'item'.

#         """
#         matches = []
#         for dictionary in self.contents:
#             try:
#                 match = dictionary.get(item)
#                 if match is not None:
#                     matches.append(match)
#                 if self.return_first:
#                     return matches[0]
#             except KeyError:
#                 pass
#         if len(matches) == 0:
#             raise KeyError(f'{item} is not found in the Corpus')
#         if len(matches) > 1:
#             return matches[0]
#         else:
#             return matches

#     """ Dunder Methods """

#     def __iter__(self) -> Iterator[Any]:
#         """Returns iterable of 'classes' and 'instances'.

#         Returns:
#             Iterator: of 'classes' and 'instances'.

#         """
#         combined = copy.deepcopy(self.instances)
#         return iter(combined.update(self.classes))

#     def __len__(self) -> int:
#         """Returns combined length of 'instances' and 'classes'.

#         Returns:
#             int: combined length of 'instances' and 'classes'.

#         """
#         return len(self.instances) + len(self.classes)


# @dataclasses.dataclass
# class Library(Anthology):
#     """Mixin for Keystone registries.

#     This should be added as a mixin to a Anthology class, depending upon what is
#     to be stored.

#     Args:
#         contents (MutableMapping[Hashable, Any]): stored dictionary. Defaults
#             to an empty Anthology instance.
#         default_factory (Optional[Any]): default value to return or default
#             callable to use to create the default value. Defaults to None.
#         name (Optional[Hashable]): name of Library, which is used by Librarian
#             to access the Library instance. Defaults to None.

#     """

#     contents: MutableMapping[Hashable, Any] = dataclasses.field(
#         default_factory = Anthology)
#     default_factory: Optional[Any] = None
#     name: Optional[Hashable] = dataclasses.field(default = camina.Name())

#     """ Initialization Methods """

#     def __post_init__(self) -> None:
#         """Automatically initializes 'name' attribute."""
#         with contextlib.suppress(AttributeError):
#             super().__post_init__()
#         self._validate_name()

#     """ Instance Methods """

#     def deposit(
#         self,
#         item: object | type[Any],
#         name: Optional[Hashable] = None) -> None:
#         """Adds 'item' to 'contents'.

#         Args:
#             item (object | type[Any]): class or instance to add to 'contents'.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using 'configuration.KEYER'.
#                 Defaults to None.

#         """
#         self.contents[name] = item
#         if not inspect.isabstract(item) and self.default_factory is None:
#             self.default_factory = self.contents[name]
#         self._validate_name()
#         return

#     """ Private Methods """

#     def _validate_name(self) -> None:
#         """Sets 'name' attribute if it is None."""
#         if self.name is None:
#             if self.contents:
#                 first_item = self.contents[next(iter(self.contents.keys()))]
#                 self.name = setup.KEYER(first_item)
#             elif self.default_factory:
#                 self.name = setup.KEYER(self.default)
#         return


# @dataclasses.dataclass
# class Librarian(Anthology, camina.ChainDictionary):
#     """Stores Keystone subclasses and/or instances.

#     For each Keystone, an attribute is added with the snakecase name of that
#     Keystone. In that attribute, a dict-like object (determined by
#     'default_factory') is the value and it stores all Keystone subclasses of
#     that type (again using snakecase names as keys).

#     If you want to use a different naming convention besides snakecase, you can
#     either:
#         1) subclass and override the '_get_name' method to only change the
#             naming convention for Librarian; or
#         2) or call 'ashford.set_keyer' to set the naming function used
#             throughout ashford.

#     Args:
#         contents (MutableSequence[Library[Hashable, Any]]): list of
#             stored Library instances.
#         default_factory (Optional[Any]): default value to return or default
#             callable to use to create the default value.
#         return_first (Optional[bool]): whether to only return the first match
#             found (True) or to search all of the stored Dictionary instances
#             (False). Defaults to False.

#     Attributes:
#         All direct Keystone subclasses will have an attribute name added
#         dynamically.

#     """

#     contents: MutableSequence[Library] = (
#         dataclasses.field(default_factory = list))
#     default_factory: type[Any] = None
#     return_first: Optional[bool] = False
#     storage: ClassVar[type[Library]] = Library

#     """ Properties """

#     @property
#     def bases(self) -> dict[Hashable, Hashable]:
#         """Returns dict of stored subclass names and their associated bases.

#         Returns:
#             dict[Hashable, Hashable]: keys are the stored subclass names and the
#                 values are the names of the base class which they are derived
#                 from.

#         """
#         bases = {}
#         for registry in self.contents:
#             bases |= dict.fromkeys(registry.keys(), registry.name)
#         return bases

#     @property
#     def defaults(self) -> dict[Hashable, Library]:
#         """Returns dict of defaults for each stored registry.

#         Returns:
#             dict[Hashable, Library]: keys are the 'name' attributes of
#                 each stored map and values are 'default' attribute.

#         """
#         return {m.name: m.default_factory for m in self.contents}

#     @property
#     def libraries(self) -> dict[Hashable, Library]:
#         """Returns dict of stored registries.

#         Returns:
#             dict[Hashable, Library]: keys are the 'name' attributes of
#                 each stored map and values are the stored maps.

#         """
#         return {m.name: m for m in self.contents}

#     @property
#     def names(self) -> list[Hashable]:
#         """Returns list of names of stored registries.

#         Returns:
#             list[Hashable]: names taken from 'name' attributes of the stored
#                 registries.

#         """
#         return [m.name for m in self.contents]

#     """ Instance Methods """

#     def add_library(self, name: Hashable) -> None:
#         """Adds a new Library instance to 'contents'.

#         Args:
#             name (Hashable): name of Library, which will be passed to the new
#                 Library instance.

#         """
#         self.contents.append(self.storage(name = name))
#         return

#     def classify(self, item: str | type[Any] | object) -> str:
#         """Returns the str name of the object of which 'item' is.

#         Args:
#             item (str | type[Any] | object): object, class, or str name of an
#                 object or class.

#         Raises:
#             ValueError: if 'item' does not match a subclass of any recognized
#                 type.

#         Returns:
#             str: snakecase str name of the base type of which 'item' is a
#                 subclass or subclass instance.

#         """
#         if not inspect.isclass(item) and not isinstance(item, str):
#             testable = item.__class__
#         else:
#             testable = item
#         for name, library in self.libraries.items():
#             if isinstance(testable, str):
#                 match = library.get(testable, None)
#                 if match is not None:
#                     return name
#             else:
#                 for value in library.values():
#                     if issubclass(testable, value):
#                         return name
#         raise ValueError(f'{item} is not a subclass of any recognized type')

#     def deposit(
#         self,
#         item: object | type[Any],
#         name: Optional[Hashable] = None) -> None:
#         """Adds 'item' to 'contents'.

#         Args:
#             item (object | type[Any]): item to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using '_get_name'. Defaults to
#                 None.

#         """
#         try:
#             base = self.classify(item = item)
#             self._deposit_to_existing(item = item, name = name, base = base)
#         except ValueError:
#             self._desposit_to_new(item = item, name = name)
#         return

#     # def validate(
#     #     self,
#     #     item: object,
#     #     attribute: str,
#     #     parameters: Optional[MutableMapping[Hashable, Any]] = None) -> object:
#     #     """Creates or validates 'attribute' in 'item'.

#     #     Args:
#     #         item (object): object (often a Project or Manager instance) of which
#     #             a Keystone in 'attribute' needs to be validated or
#     #             created.
#     #         attribute (str): name of the attribute' in item containing a value
#     #             to be validated or which provides information to create an
#     #             appropriate instance.
#     #         parameters (Optional[MutableMapping[Hashable, Any]]): parameters to pass
#     #             to or inject in the Keystone subclass instance.

#     #     Raises:
#     #         ValueError: if the value of 'attribute' in 'item' does match any
#     #             known subclass or subclass instance of that Keystone
#     #             subtype.

#     #     Returns:
#     #         object: completed, linked instance.

#     #     """
#     #     parameters = parameters or {}
#     #     instance = None
#     #     # Get current value of 'attribute' in 'item'.
#     #     value = getattr(item, attribute)
#     #     # Get the corresponding base class.
#     #     base = self.bases[attribute]
#     #     # Gets the relevant registry for 'attribute'.
#     #     registry = getattr(self, attribute)
#     #     # Adds parameters to 'value' is already an instance of the appropriate
#     #     # base type.
#     #     if isinstance(value, base):
#     #         for parameter, argument in parameters.items():
#     #             setattr(value, parameter, argument)
#     #         instance = value
#     #     # Selects default class for 'attribute' if none exists.
#     #     elif value is None:
#     #         name = self.defaults[attribute]
#     #         if name:
#     #             value = registry[name]
#     #         else:
#     #             raise ValueError(
#     #                 f'Neither a value for {attribute} nor a default class '
#     #                 f'exists')
#     #     # Uses str value to select appropriate subclass.
#     #     elif isinstance(value, str):
#     #         name = getattr(item, attribute)
#     #         value = registry[name]
#     #     # Gets name of class if it is already an appropriate subclass.
#     #     elif inspect.issubclass(value, base):
#     #         name = configuration.KEYER(value)
#     #     else:
#     #         raise ValueError(f'{value} is not a recognized keystone')
#     #     # Creates a subclass instance.
#     #     if instance is None:
#     #         instance = value.create(name = name, **parameters)
#     #     setattr(item, attribute, instance)
#     #     return item

#     """ Private Methods """

#     def _deposit_to_existing(
#         self,
#         item: object | type[Any],
#         name: Optional[Hashable],
#         base: Hashable) -> None:
#         """Adds 'item' to an existing Library in 'contents'.

#         Args:
#             item (object | type[Any]): item to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using '_get_name'.
#             base (Hashable): name of the Library to add 'item' to.

#         """
#         name = self._get_name(item = item, name = name)
#         library = self.libraries[base]
#         library.deposit(item = item, name = name)
#         return

#     def _desposit_to_new(
#         self,
#         item: object | type[Any],
#         name: Optional[Hashable]) -> None:
#         """Adds 'item' to a new Library in 'contents'.

#         Args:
#             item (object | type[Any]): item to add to the registry.
#             name (Optional[Hashable]): key to use to store 'item'. If not
#                 passed, a key will be created using '_get_name'.

#         """
#         name = self._get_name(item = item, name = name)
#         self.add_library(name = name)
#         self.libraries[name][name] = item
#         return

#     def _get_name(
#         self,
#         item: type[Any],
#         name: Optional[str] = None) -> None:
#         """Returns 'name' or str name of item.

#         By default, the method uses configuration.KEYER to create a snakecase name.
#         If the resultant name begins with any prefix listed in
#         defaults.REMOVABLE_PREFIXES, that substring is removed.

#         If you want to use another naming convention, just subclass and override
#         this method. All other methods will call this method for naming.

#         Args:
#             item (type[Any]): item to name.
#             name (Optional[str], optional): optional name to use. A 'project_'
#                 prefix will be removed, if it exists. Defaults to None.

#         Returns:
#             str: name of 'item' or 'name' (with the 'project' prefix removed).

#         """
#         name = name or setup.KEYER(item)
#         if name.startswith(tuple(setup.REMOVABLE_PREFIXES)):
#             for prefix in setup.REMOVABLE_PREFIXES:
#                 name.dropprefix(prefix)
#         return name

#     # """ Dunder Methods """

#     # def __getattr__(self, attribute: Hashable) -> Library:
#     #     """Returns Library that has a 'name' matching 'attribute'.

#     #     Args:
#     #         attribute (Hashable): name of attribute sought.

#     #     Returns:
#     #         Library: a Library instance stored in 'contents'.

#     #     """
#     #     return self.libraries[attribute]


# # """ Registrar Decorator """

# # @dataclasses.dataclass
# # class registered(object):
# #     """Decorator that automatically registers wrapped class or function.

# #     registered violates the normal python convention of naming classes in
# #     capital case because it is only designed to be used as a callable decorator,
# #     where lowercase names are the norm.

# #     All registered functions and classes are stored in the 'registry' class
# #     attribute of the wrapped item (even if it is a function). So, it is
# #     accessible with '{wrapped item name}.registry'. If the wrapped item is a
# #     class is subclassed, those subclasses will be registered as well via the
# #     '__init_subclass__' method which is copied from the Registrar class.

# #     Wrapped functions and classes are automatically added to the stored registry
# #     with the 'keyer' function. Virtual subclasses can be added using the
# #     'register' method which is automatically added to the wrapped function or
# #     class.

# #     Args:
# #         wrapped (Callable[..., Optional[Any]]): class or function to be stored.
# #         default (dict[str, Callable[..., Optional[Any]]]): any items to include
# #              in the registry without requiring additional registration. Defaults
# #              to an empty dict.
# #         keyer (Callable[[Any], str]): function to infer key names of wrapped
# #             functions and classes. Defaults to the 'namify' function in ashford.

# #     """
# #     wrapped: Callable[..., Optional[Any]]
# #     defaults: dict[str, Callable[..., Optional[Any]]] = dataclasses.field(
# #         default_factory = dict)
# #     keyer: Callable[[Any], str] = dataclasses.field(default = configuration.KEYER)

# #     """ Initialization Methods """

# #     def __call__(
# #         self,
# #         *args: Any,
# #         **kwargs: Any) -> Callable[..., Optional[Any]]:
# #         """Allows class to be called as a decorator.

# #         Returns:
# #             Callable[..., Optional[Any]]: callable after it has been registered.

# #         """
# #         # Updates 'wrapped' for proper introspection and traceback.
# #         functools.update_wrapper(self, self.wrapped)
# #         # Copies key attributes and functions to wrapped item.
# #         self.wrapped.register = self.register
# #         self.wrapped.registry = self.__class__.registry
# #         if inspect.isclass(self.wrapped):
# #             self.wrapped.__init_subclass__ = base.Registrar.__init_subclass__
# #         return self.wrapped(*args, **kwargs)

# #     """ Properties """

# #     @property
# #     def registry(self) -> MutableMapping[Hashable, type[Any]]:
# #         """Returns internal registry.

# #         Returns:
# #             MutableMapping[Hashable, type[Any]]: dict of str keys and values of
# #                 registered items.

# #         """
# #         if self.defaults:
# #             complete = copy.deepcopy(self._registry)
# #             complete.update(self.defaults)
# #             return complete
# #         else:
# #             return self._registry

# #     """ Public Methods """

# #     @classmethod
# #     def register(cls, item: type[Any], name: Optional[str] = None) -> None:
# #         """Adds 'item' to 'registry'.

# #         """
# #         # The default key for storing cls is its snakecase name.
# #         key = name or cls.keyer(cls)
# #         cls.registry[key] = item
# #         return


# @dataclasses.dataclass
# class Keystone(abc.ABC):
#     """Mixin for core package base classes.

#     Attributes:
#         registry (ClassVarLibrarian]): stores subclasses and/or instances.

#     """

#     registry: ClassVar[Librarian]

#     """ Class Methods """

#     @classmethod
#     def set_registry(cls, registry: Librarian | type[Librarian]) -> None:
#         """Assigns 'registry' class attribute to 'registry' argument.

#         Args:
#             registry (registry: Librarian | Type[Librarian]): registry to store
#                 Keystone subclasses and/or subclass instances.

#         Raises:
#             TypeError: if 'registry' is not a subclass or subclass instance of
#                 Librarian.

#         """
#         if issubclass(registry, Librarian):
#             cls.registry = registry()
#         elif isinstance(registry, Librarian):
#             cls.registry = registry
#         else:
#             raise TypeError(
#                 'registry must be a subclass or subclass instance of Librarian')
#         return


# @dataclasses.dataclass
# class CuratorKeystone(
#     Keystone, registrars.Curator, factories.AnthologyFactory, abc.ABC):
#     """Mixin for core package base classes.

#     Attributes:
#         registry (ClassVar[Librarian]): stores subclasses and instances.
#             Defaults to an empty CorpusLibrarian.

#     """

#     registry: ClassVar[Librarian] = Librarian()


# @dataclasses.dataclass
# class InstancerKeystone(
#     Keystone, registrars.Instancer, factories.AnthologyFactory, abc.ABC):
#     """Mixin for core package base classes.

#     Attributes:
#         registry (ClassVar[Librarian]): stores subclass instances. Defaults to
#             an empty AnthologyLibrarian.

#     """

#     registry: ClassVar[Librarian] = Librarian()


# @dataclasses.dataclass
# class SubclasserKeystone(
#     Keystone, registrars.Subclasser, factories.AnthologyFactory, abc.ABC):
#     """Mixin for core package base classes.

#     Attributes:
#         registry (ClassVar[Librarian]): stores subclasses. Defaults to
#             an empty AnthologyLibrarian.

#     """

#     registry: ClassVar[Librarian] = Librarian()
