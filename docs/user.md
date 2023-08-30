# User Guide

## Factories

All `wonka` factory classes have a `create` class method which is used to construct new items. The only required parameter for `create` is `item`, which contains the data for building products. Other parameters are optional, but may be used for greater functionality, particularly in regard to `Producer` mixins, discussed below.

These are the registry factory classes. Keys for any registry-style factory follow the naming convention of the global setting `_KEY_NAMER` (defaults to snakecase) which may be changed with `set_keyer`. These are the registration-style classes:

* `Registrar`: a factory that creates items from data stored in the `registry` class attribute (which may be any dict-like object).
* `Subclasser`: mixin that acts like a `Registrar`, but without the `registry` attribute. Instead, the class creates a dictionary facade at runtime by drawing data from the `__subclasses__` attribute of every class.

The second type of factory is dispatch. These factories will call creation class methods of subclasses that follow the naming convention of `_METHOD_NAMER` (`f'from_{snakecase(substring))}'` by default) which may be changed with `set_method_namer`. These are the dispatcher factories:

* `Sourcerer`: calls the appropriate creation class method based on the type of the first passed argument. The keys of `sources` are types which the `item` argument may either be instances of subclasses of those types to trigger the dispatching to the appropriate creation method.
* `Delegate`: similar to `Sourcerer`, but it does not have a `sources` attribute. Instead, it uses the string name of the type of the `item` argument. This is far less forgiving than the process used by `Sourcerer` and should only be used if you are absolutely sure that the string names of the `item` arguments will always correspond with a creation method in the `Delegate`.

The final type of factory, the prototypers, clone existing classes or objects. Out of the box, `wonka` includes just one prototyper:

* `Scribe`: creates a [deep copy](https://docs.python.org/3/library/copy.html) of an existing object or class. If mixed in with certain `Producer` subcclasses, it can add, modify, or delete existing attributes of the cloned object in its copy.

Regardless of whether your new factory design fits one of the above categories, any new factories may be added by simply subclassing `Factory`.


Here is a simple example of a `Subclasser` factory.

```python
import dataclasses
import wonka


# wonka uses dataclasses because they are easier to read at a glance, but you
# may use standard classes, if you would prefer.
@dataclasses.dataclass
class Base(wonka.Subclasser):
    
    name: str
    identification: int


@dataclasses.dataclass
class DirectSubclass(Base):
    
    name: str
    identification: int


@dataclasses.dataclass
class IndirectSubclass(DirectSubclass):
    
    name: str
    identification: int


# If you just want to construct a class:
my_class = Base.create('indirect_subclass')

# If you would prefer to create an instance of a subclass instead:
parameters = {'name' = 'Ada Lovelace', identification = 1815}
my_instance = Base.create('indirect_subclass', parameters)
```

That's all you need to do to create a subclass and subclass instance of `Base` without any registry attribute cluttering the namespaces of any of the classes. `Subclasser` accomplishes this by taking advantage of the `__subclassess__` attribute of every class and, by default, recursively searches for all subclasses of those subclasses (since the `__subclassess__` attribute only includes direct subclasses). It then uses the global setting for creating keys of this implicit registry for constructing a dictionary interface on the fly. If you would prefer a different naming convention for registry keys, you can easily change it from the default of snakecase by using the "set_keyer" function. If you would instead prefer a formal, declared registry for your factory (particularly useful if you have a large number of subclasses or items that are not subclasses), you can subclass the `Registrar` class instead.

But, what if you want the `create` method to always return an instance instead of a class, even when `parameters` are not passed? That's easy. You would just add `Instancer` as a mixin as follows:

```python
@dataclasses.dataclass
class Base(wonka.Instancer, wonka.Subclasser):
    
    name: str
    identification: int
```

Or, conversely, if you wanted to always return a class (and ignore any parameters), you could add the `Classer` mixin instead.

Here is a real-world example using a different type of factory: the `Sourcerer`. It works by calling creation class methods based on the type of data passed to the `create` method. This example is adapted from the [`bobbie`](https://github.com/WithPrecedent/bobbie) library, which offers a flexible system for project configuration settings.

```python
from __future__ import annotations
from collections.abc import Hashable, MutableMapping
import configparser
import dataclasses
from typing import Any, ClassVar, Optional, Type

import wonka


@dataclasses.dataclass
class Settings(wonka.Sourcerer):
    
    contents: MutableMapping[Hashable, Any] = dataclasses.field(
        default_factory = dict)
    defaults: Optional[MutableMapping[Hashable, Any]] = dataclasses.field(
        default_factory = dict)
    infer_types: Optional[bool] = True
    sources: ClassVar[MutableMapping[type[Any], str]] = {
        MutableMapping, 'dictionary',
        pathlib.Path, 'path',
        str, 'path'}

    @classmethod
    def from_dictionary(cls, item: MutableMapping[Hashable, Any]) -> Settings:
        """Creates a Settings instance from a dict-like object."""      
        return cls(contents = item)
        
    @classmethod
    def from_path(cls, item: str | pathlib.Path) -> Settings:
        """Creates a Settings instance from an .ini file."""
        path = pathlib.Path(item) if str else path  
        contents = configparser.ConfigParser(dict_type = dict)
        contents.optionxform = lambda option: option
        contents.read(path)
        return cls(contents = dict(contents._sections))
    
parameters = {'defaults': {'verbose': True}, 'infer_types': False}
# The 'create' class method detects the data type of the first argument passed 
# and calls the appropriate construction method based on its type. Unlike 
# ordinary dispatch systems, Sourcerer tests whether the passed argument is 
# a subclass or subclass instance of the types included in the 'sources' class 
# attribute.
initialization = Settings.create('some_path.ini', parameters = parameters)
```

The `create` method which is inherited from `Sourcerer` automatically calls the `from_path` method because the `item` argument is a string. All you need to provide in your class is the "`from_`" creation methods and the `sources` class attribute. The dispatching is then handled by `Sourcerer`. If you would prefer an alernate naming convention for the creation methods, you can change that with `set_method_namer`.

## Managers

So, you can have 'Manager' subclass instances in your iteratable constructors (instead of just `Factory` subclasses). Any type of Iterable can be used as long as it returns a consistent, compatiable datatype at each iteration. Out-of-the-box, `wonka` includes a basic sequential `Manager` called `Assembler` which acts like a simple assembly line constructor.

## Producers

Producers are mix-ins for any `Factory` class that apply automatic, seamless changes before classes or objects are returned by the `wonka` factories Out-of-the-box, all `wonka` factories check to see if an Producer is mixed in before returning the completed project. `wonka` includes these producers:

* `Classer`: Always changes a factory's product to a class.
* `Flexer`: Conditions a factory's product type on whether a `parameters` argument is passed. If `parameters` are passed, an instance is always returned. Otherwise, the product is left as is.
* `Instancer`: Always changes a factory's product to an instance.

To add your own class, simply subclass `Producer` with a `produce` class method. So, for example, if you are working with datasets and want your Factory to always return a [Numpy](https://github.com/numpy/numpy) array, you should mix in a Producer that would convert other datatypes to that format.

## Interoperability

Notably, `wonka` is 100% compatible with my other project framework libraries, of which it was originally a part. This is why you should feel confident in the continued development and maintenance of the library - it is essential part of my overall work. I have decided to make it available as a separate library for those that just want to use its implementation without the other components of my project framework ecosystem. So, for example, any of the many registry types of [ashford](https://github.com/WithPrecedent/ashford) can be used with a `Registrar` in `wonka`. Further, for project workflow pipelining, where dynamic factories are essential, the `wonka` classes are interwoven and can be extended in the [chrisjen](https://github.com/WithPrecedent/chrisjen) and [amos](https://github.com/WithPrecedent/amos) packages. Also, for those using configuration option files, `wonka` is supported by the [bobbie](https://github.com/WithPrecedent/bobbie) project settings library. So, I, and any other maintainers, will do my best to promptly integrate any contributions.

### Helpers

In addition to the core classes described above, `wonka` includes other convenience classes and functions, each of which is outlined below.

The library includes `Manufacturer`, a dictionary of factories, if you want all of your project factories in one location and runtime addition and subtraction of factories.

`wonka` also includes convenience functions for changing global settings that set naming conventions for registry keys and creation method names. Those methods and settings are:

* `set_compatibility_rule` sets whether `wonka` runs a validation check to see if a prospective factory is either a subclass of `Factory` or a subclass instance of `Manager`. If True, strict inheritance will be enforced. If False, no check will be performed and any incompatibility will only be discovered when the constructor's `create` method is called. The value for this setting is stored in `_STRICT_COMPATIBILITY` and defaults to True.
* `set_keyer` may be used to change the global value of `_KEY_NAMER`, which controls the naming convention for registry dictionary keys in `wonka`. This is particularly important for `Subclasser`, which automatically creates keys based on a class' `__subclasses__` attribute. By default, `_KEY_NAMER' infers a snakecase name of any passed value.
* `set_method_namer` may be used to change the global value of the `_METHOD_NAMER`, which controls the naming convention for creation method names used in dispatcher factories. By default `_METHOD_NAMER` uses a prefix of 'from_' followed by the snakecase name of the type of the passed `item` argument. So, as the example above indicates, a class method named `from_path` is used for creating a `Settings` instance from a file path.
* `set_overwrite_rule` sets whether existing attributes are overwritten when parameters are passed to a factory `create` method. This situation only arises with a registry-based factory stores at least some instances (instead of just classes). In such a situation, if the value is set to True, the passed parameters will be injected and overwrite any existing values. If False, no existing values will be overwritten, even if a parameter with the same attribute name is passed. The value for this setting is stored in `_OVERWRITE` and defaults to True.