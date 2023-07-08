# wonka

<p align="center">
<img src="./img/top_hat.png" alt="wonka top hat logo" style="width:250px;"/>
</p>

[![PyPI Latest Release](https://img.shields.io/pypi/v/wonka.svg?style=for-the-badge&logo=PyPI)](https://pypi.org/project/wonka/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=for-the-badge&logo=github)](https://WithPrecedent.github.io/wonka)
![Code Coverage](https://img.shields.io/codecov/c/github/WithPrecedent/wonka?style=for-the-badge&logo=codecov&logoColor=white)
[![PDM Managed](https://img.shields.io/badge/pdm-managed-blueviolet?style=for-the-badge)](https://pdm.fming.dev)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge&logo=apache)](https://opensource.org/licenses/Apache-2.0)
<!-- ![GitHub Actions](https://img.shields.io/github/actions/workflow/status/WithPrecedent/wonka/actions?style=for-the-badge&logo=githubactions&logoColor=white) -->

## What is wonka?

`wonka`[^1] is an extensible library that enables simple implementation of class and object constructors in Python. Out-of-the-box, `wonka` includes various creational design patterns, from registry factories to prototypers to composite builder workflows. It is also easy to add custom factories,[^2] while taking advantage of `wonka`'s convenient mixin classes and helper functions. This readme file offers a basic outline of how `wonka` works. If you would prefer to jump right into the full documentation, go [here](https://WithPrecedent.github.io/wonka).

## Why use wonka?

<p align="center">
<img src="https://media.giphy.com/media/y0SJVYxf90J1u/giphy.gif" alt="The suspense is terrible. I hope it'll last" style="width:300px;"/>
</p>

*“No other factory in the world mixes its chocolate by waterfall… But it’s the only way if you want it just right.”* - Willy Wonka

Factories are essential components of coding projects that require dynamic, runtime implementation of different strategies or options. In Python packages, despite their commmon usage, factories are often poorly implemented, fragile, or inflexible. `wonka` addresses those common shortcomings by offering convenient creation through a simple, adaptable system that has almost no learning curve[^3]. `wonka` is:

* **Intuitive**: factories use a common interface with a `create` class method for all construction operations.
* **Extensible**: core classes can be adapted and extended through inheritance or composition.
* **Lightweight**: the library has a miniscule memory footprint with few dependencies.
* **Robust**: "turn-key" factories handle edge cases and core scenarios without needing further tinkering.
* **Accessible**: `wonka` is over-documented to make it accessible to beginnning coders and readily usable for developers at all levels.

## Getting started

<p align="center">
<img src="https://media4.giphy.com/media/Tt9jctxaVjRny/giphy.gif" alt="Please, tell us more" style="width:350px;"/>
</p>

### Installation

To install `wonka`, use `pip`:

```sh
pip install wonka
```

### Usage

Here is a simple example using a `Subclasser` factory.

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

That's all you need to do to create a subclass and subclass instance of `Base` without any registry attribute cluttering the namespaces of any of the classes. `Subclasser` accomplishes this by taking advantage of the `__subclassess__` attribute of every class and, by default, recursively searches for all subclasses of those subclasses until there are no more to be found (since the `__subclassess__` attribute only includes direct subclasses). It then uses the global setting for creating keys of this implicit registry for constructing a dictionary interface on the fly. If you would prefer a different naming convention for registry keys, you can easily change it from the default of snakecase by using the "set_keyer" function. If you would instead prefer a formal, declared registry for your factory (particularly useful if you have a large number of subclasses), you can subclass the `Registrar` class instead.

But, what if you want the `create` method to always return an instance instead of a class, even when `parameters` are not passed? That's easy. You would just add `Instancer` as a mixin as follows:

```python
@dataclasses.dataclass
class Base(wonka.Instancer, wonka.Subclasser):
    
    name: str
    identification: int
```

Or, conversely, if you wanted to always return a class (and ignore any parameters), you could add the `Classer` mixin instead.

Here is a real-world example using a different type of factory: the `Sourcerer`. It works by calling creation class methods based on the type of data passed to the `create` method. This example is adapted from the [bobbie](https://github.com/WithPrecedent/bobbie) library, which offers a flexible system for project configuration settings.

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

For examples using the rest of `wonka`'s factories, check out the Examples section of the documentation.

## How does wonka work?

There are three categories of base classes in `wonka`: factories, managers, and producers. Each is described in greater detail below, followed by discussion of other convenience classes and functions included with `wonka`.

### Factories

<p align="center">
<img src="https://media2.giphy.com/media/o4aGs2I3rVKjC/giphy.gif" alt="Come with me and you'll be in a world of pure imagination" style="width:350px;"/>
</p>

Out-of-the-box, this library offers three general styles of its base `Factory` class. These are not subclasses, but rather describe the type of functionality in the included `Factory` subclasses.

* Registries - factories that build classes or objects from explicit or implicit registries.
* Dispatchers - factories that call appropriate creation methods or functions based on the type or content of data passed.
* Prototypers - factories that clone exsting classes or objects.

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

### Managers

<p align="center">
<img src="https://media.giphy.com/media/NsBAHgohHByp2/giphy.gif" alt="Don't just stand there! Do something!" style="width:300px;"/>
</p>

For more complex construction, you can use subclasses of `Manager`, which is an iterable constructor. Every `Manager` subclass may construct items in three ways:

1. Calling its `manage` method.
2. Calling its `create` method (which just calls the `manage` method, but this allows a `Manager` subclass instance to be used anywhere a `Factory` could be used).
3. Iterating it directly.

So, you can have 'Manager' subclass instances in your iteratable constructors (instead of just `Factory` subclasses). Any type of Iterable can be used as long as it returns a consistent, compatiable datatype at each iteration. Out-of-the-box, `wonka` includes a basic sequential `Manager` called `Assembler` which acts like a simple assembly line constructor.

### Producers

<p align="center">
<img src="https://media4.giphy.com/media/l0HlHSB8v5yRtBlHW/giphy.gif" alt="Willy Wonka completes a forward roll and pops up" style="width:350px;"/>
</p>

As another optional feature, `wonka` supports post-construction modification of built items through subclasses of `Producer`. This is particularly important for factories that use other resources (such as registries). `wonka` [separates concerns](https://dev.to/suspir0n/soc-separation-of-concerns-5ak7) so that the return value can be modified through a simple mixin system. This division of labor makes it incredibly easy to put together any `Factory` with any `Producer`.

Producers are mix-ins for any `Factory` class that apply automatic, seamless changes before classes or objects are returned by the `wonka` factories Out-of-the-box, all `wonka` factories check to see if an Producer is mixed in before returning the completed project. `wonka` includes these producers:

* `Classer`: Always changes a factory's product to a class.
* `Flexer`: Conditions a factory's product type on whether a `parameters` argument is passed. If `parameters` are passed, an instance is always returned. Otherwise, the product is left as is.
* `Instancer`: Always changes a factory's product to an instance.

To add your own class, simply subclass `Producer` with a `produce` class method. So, for example, if you are working with datasets and want your Factory to always return a [Numpy](https://github.com/numpy/numpy) array, you should mix in a Producer that would convert other datatypes to that format.

### Helpers

In addition to the core classes described above, `wonka` includes other convenience classes and functions, each of which is outlined below.

The library includes `Manufacturer`, a dictionary of factories, if you want all of your project factories in one location and runtime addition and subtraction of factories.

`wonka` also includes convenience functions for changing global settings that set naming conventions for registry keys and creation method names. Those methods and settings are:

* `set_compatibility_rule` sets whether `wonka` runs a validation check to see if a prospective factory is either a subclass of `Factory` or a subclass instance of `Manager`. If True, strict inheritance will be enforced. If False, no check will be performed and any incompatibility will only be discovered when the constructor's `create` method is called. The value for this setting is stored in `_STRICT_COMPATIBILITY` and defaults to True.
* `set_keyer` may be used to change the global value of `_KEY_NAMER`, which controls the naming convention for registry dictionary keys in `wonka`. This is particularly important for `Subclasser`, which automatically creates keys based on a class' `__subclasses__` attribute. By default, `_KEY_NAMER' infers a snakecase name of any passed value.
* `set_method_namer` may be used to change the global value of the `_METHOD_NAMER`, which controls the naming convention for creation method names used in dispatcher factories. By default `_METHOD_NAMER` uses a prefix of 'from_' followed by the snakecase name of the type of the passed `item` argument. So, as the example above indicates, a class method named `from_path` is used for creating a `Settings` instance from a file path.
* `set_overwrite_rule` sets whether existing attributes are overwritten when parameters are passed to a factory `create` method. This situation only arises with a registry-based factory stores at least some instances (instead of just classes). In such a situation, if the value is set to True, the passed parameters will be injected and overwrite any existing values. If False, no existing values will be overwritten, even if a parameter with the same attribute name is passed. The value for this setting is stored in `_OVERWRITE` and defaults to True.

## Contributing

Contributors are always welcome and should find `wonka` easy to work with. The project is highly documented so that users and developers can make `wonka` work with their projects. It is designed for Python coders at all levels. Even beginners should be able to follow the readable code and internal documentation to understand how it works. If you wish to contribute, please read the [Contribution Guide](./contributing.md) and [Code of Conduct](./code_of_conduct.md).

Notably, `wonka` is 100% compatible with my other project framework libraries, of which it was originally a part. This is why you should feel confident in the continued development and maintenance of the library - it is essential part of my overall work. I have decided to make it available as a separate library for those that just want to use its implementation without the other components of my project framework ecosystem. So, for example, any of the many registry types of [ashford](https://github.com/WithPrecedent/ashford) can be used with a `Registrar` in `wonka`. Further, for project workflow pipelining, where dynamic factories are essential, the `wonka` classes are interwoven and can be extended in the [chrisjen](https://github.com/WithPrecedent/chrisjen) and [amos](https://github.com/WithPrecedent/amos) packages. Also, for those using configuration option files, `wonka` is supported by the [bobbie](https://github.com/WithPrecedent/bobbie) project settings library. So, I, and any other maintainers, will do my best to promptly integrate any contributions.

## Similar Projects

If `wonka` does not fit your needs, you might find one of these other packages helpful. None of them does the same things that `wonka` does (which is why I created this library), but they might fit your particular project needs better.

<p align="center">
<img src="https://media.giphy.com/media/Bu8ADbj7NuRry/giphy.gif" alt="Stop. Don't. Come back." style="width:300px;"/>
</p>

* [dataclass_factory](https://github.com/reagento/dataclass-factory): factory for dataclass production from other common data types.
* [factory_boy](https://github.com/FactoryBoy/factory_boy): tool for dynamically creating objects for unit testing in Python.
* [Model Bakery](https://github.com/model-bakers/model_bakery): object factory for Django.
* [Polyfactory](https://github.com/litestar-org/polyfactory): factory framework for mock data generation.

## Acknowledgements

[PDM](https://github.com/pdm-project/pdm) and [MkDocs](https://github.com/mkdocs/mkdocs) made my `wonka` development workflow better and easier. I'd also like to extend a special thanks to [pawamoy](https://github.com/pawamoy) whose excellent PDM and Mkdocs extensions and utlities are incorporated into `wonka`. The scripts, documentation, configuration files, and other CI code were all adapted (or simply copied) from pawamoy's repositories.

I would also like to thank the University of Kansas School of Law for tolerating and supporting this law professor's coding efforts, an endeavor which is well outside the typical scholarly activities in the discipline.

Lastly, I want to extend a special thanks to the late, great Gene Wilder, whose work inspired the name of this project and made my childhood better.

<p align="center">
<img src="https://media.giphy.com/media/3o6ZtbOoOHu28ftYiI/giphy.gif" alt="RIP, Gene Wilder, 1933-2016" style="width:200px;"/>
</p>

[^1]: This project is not affiliated with Willy Wonka candy, either of the Willy Wonka films (especially the Johnny Depp one), or any other Willy Wonka product. It's just named "wonka" because all of the most obvious names for a Python package of factories and other constructors on [pypi.org](https://pypi.org) were taken and Willy Wonka's insane candy factory was the first relevant pop-culture touchstone I could think of.

[^2]: For the sake of brevity, the documentation refers to all of `wonka`'s constructors as "factories," even though many do not fit the definition of the classic [factory design pattern](https://realpython.com/factory-method-python/).

[^3]: Chocolate waterfalls are, sadly, only virtually implemented in `wonka`.
