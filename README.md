# What is `wonka`?

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![PyPI Latest Release](https://img.shields.io/pypi/v/wonka.svg)](https://pypi.org/project/wonka/) 
<!-- [![CI](https://github.com/wonka/wonka/workflows/CI/badge.svg?event=push)](https://github.com/wonka/wonka/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![Coverage](https://coverage-badge.samuelcolvin.closers.dev/wonka/wonka.svg)](https://coverage-badge.samuelcolvin.closers.dev/remanage/wonka/wonka) -->
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 
[![Documentation Status](https://readthedocs.org/projects/wonka/badge/?version=latest)](http://wonka.readthedocs.io/?badge=latest)

<p align="center">
<img src="https://media3.giphy.com/media/Bp5dwyOW9BwbK/giphy.gif?cid=ecf05e47fc69a9e2fe4b535c1c0a0d2641496a30302482d2&rid=giphy.gif&ct=g" height="300"/>
</p>

*“No other factory in the world mixes its chocolate by waterfall… But it’s the only way if you want it just right.”* - Willy Wonka

`wonka` provides a lightweight, extensible, accessible framework for implementing class and object constructers in Python. Out-of-the-box, this package offers three general styles of its base `Factory` class:

* Dispatchers - factories that call appropriate creation methods or functions based on the type of data passed. 
* Prototypers - factories that clone exsting classes or objects.
* Registries - factories that build classes or objects from explicit or implicit registries. 

Within those two categories of factories are four subtype implementations: `Registrar`, `Subclasser`, `Sourcerer`, and `Delegate`. All wonka factories have a simple, consistent interface that uses a `create` class method for all construction operations. The package also includes `Manufacturer`, a dictionary of factories, if you want all of your project factories in one location and runtime addition and subtraction of factories.

As an optional feature, `wonka` supports post-construction modification of built items through subclasses of `Producer`. This division of labor makes it incredibly easy to put together any `Factory` with any `Producer`. Producers are mix-ins for any `Factory` class that apply automatic, seamless changes before classes or objects are returned by the `wonka` factories. Out of the box, there are three Producer classes: `Classer`, `Flexer`, and `Instancer`. It is simple to make your own `Producer` subclasses and add them to any `wonka` factory (or your own custom factories). All `wonka` closers have an `produce` class method for for modifying objects. That `produce` method is automatically called by the `create` method of factories and does not ever need to be separately called by the user.

# Why use `wonka`?

<p align="center">
<img src="https://media4.giphy.com/media/Tt9jctxaVjRny/giphy.gif?cid=ecf05e47c18de94d59170ec6b6352617b17b841ee0bfe8a2&rid=giphy.gif&ct=g" height="300"/>
</p>

Factories are an essential component of any project that requires dynamic, runtime implementation. The goal of `wonka` is to meet that common need with a flexible system that has almost no learning curve. Significantly, `wonka` is very lightweight and efficient. It does not include any extra dependencies or code that, with large-scale project management packages, can syphon off needed resources.

`wonka` saves you having to write boilerplate while offering a highly-accessible and extensible framework for modifying factories in your Python projects. Even though factories are a basic design pattern that every coder learns, they are often poorly implemented on an ad hoc basic in Python packages. `wonka` simplifies the factory implementation process through a consistent, but flexible, interface.

Also, `wonka` is 100% compatible with my other project framework packages, of which it was originally a part. I have decided to make it available as a separate package for those that just want to use its implementation without the other components of my project framework ecosystem. So, for example, any of the many registry types of [ashford](https://github.com/WithPrecedent/ashford) can be used with a `Registrar` in `wonka`. Further, for project workflow pipelining, where dynamic factories are essential, the `wonka` classes are interwoven and can be extended in the [chrisjen](https://github.com/WithPrecedent/chrisjen) and [amos](https://github.com/WithPrecedent/amos) packages. Also, for those using configuration option files, `wonka` is supported by the [bobbie](https://github.com/WithPrecedent/bobbie) project settings package.



# Using `wonka`

## Installation

To install `wonka`, use `pip`:

```sh
pip install wonka
```
## Usage

Here is an adapted example application from the [bobbie](https://github.com/WithPrecedent/bobbie) package, which subclasses the wonka.Sourcerer:

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
    sources: ClassVar[MutableMapping[Type[Any], str]] = {
        MutableMapping, 'dictionary',
        pathlib.Path, 'path',
        str, 'path'}

    @classmethod
    def from_dictionary(cls, source: MutableMapping[Hashable, Any]) -> Settings:
        """Creates a Settings instance from a dict-like object."""      
        return cls(contents = source)
        
    @classmethod
    def from_path(cls, source: str | pathlib.Path) -> Settings:
        """Creates a Settings instance from an .ini file."""
        path = pathlib.Path(item) if str else path  
        contents = configparser.ConfigParser(dict_type = dict)
        contents.optionxform = lambda option: option
        contents.read(path)
        return cls(contents = dict(contents._sections))
    
# These will be used by the default Producer to instance the stored class.
parameters = {'defaults': {'verbose': True}, 'infer_types': False}
# The 'create' class method detects the data type of the first argument passed 
# and calls the appropriate construction method based on its type. Unlike 
# ordinary dispatch systems, Sourcerer tests whether the passed argument is 
# a subclass or subclass instance of the types included in the 'sources' class 
# attribute.
initialization = Settings.create('some_path.ini', parameters = parameters)
```

That's it. The `create` method which is inherited from `Sourcerer` automatically calls the `from_path` method because the `source` argument is a string. All you need to provide in your class is the `from_` creation methods and the `sources` class attribute. The dispatching is then handled by `Sourcerer`.

There are three categories of classes and functions in `wonka`: factories, closers, and global settings. Each is described in greater detail below.

### Factories

<p align="center">
<img src="https://media2.giphy.com/media/o4aGs2I3rVKjC/giphy.gif?cid=ecf05e47xh1nql9hj40xr8pa3tmen32e7nj2463s8pnwywi9&rid=giphy.gif&ct=g" height="300"/>
</p>

All `wonka` factory classes have a `create` class method which is used to construct new items. The only required parameter for `create` is `source`, which contains the data for building products. Other parameters are optional, but may be used for greater functionality, particularly in regard to `Producer` subclasses, discussed below.

There are two basic types of factories in wonka. The first type relies on an explicit or implicit registry of items that can serve as the basis for new item construciton. These are the catalog-type factories:
* `Registrar`: a factory that creates items from data stored in the `registry` class attribute (which may be any dict-like object).
* `Subclasser`: mixin that acts like a `Registrar`, but without the `registry` attribute. Instead, the class creates a `registry` dictionary facade at runtime by drawing data from the `__subclasses__` attribute of every class. Keys for 'registry' follow the naming convenction of the global setting `_KEY_NAMER' (defaults to snakecase).

The second type of factory is a dispatch type and are designed to exclusively work as mixins. These factories will call creation class methods of subclasses that follow the naming convention of `wonka._METHOD_NAMER` (`f'from_{snakecase(substring))}'` by default). These are the dispatcher factories:
* `Sourcerer`: mixin that calls the appropriate creation method based on the type of passed first argument and the `sources` class attribute. The keys of `sources` are types which the `source` argument may either be instances of subclasses of those types to trigger the dispatching to the appropriate creation method.
* `Delegate`: mixin similar to `Sourcerer`, but does not have a `sources` attribute. Instead, it uses the str name of the class of the `source` argument. This is far less forgiving than the process used by `Sourcerer` and should only be used if you are absolutely sure that the str names of the `source` arguments will always correspond with a creation method in the `Delegate`.

In addition, `wonka` offers a convenience dictionary for storing factories at a single location, if that is desired.
* `Manufacturer`: a dictionary of factories which acts as a convenience class if you want all of your factories in one place. It includes an `add` method for easily adding new factories, but otherwise has the interface of a python dict (and the additional functionality offered by `camina.Dictionary`).

New factories may be added by simply subclassing `wonka.Factory`.

### Producers

<p align="center">
<img src="https://media4.giphy.com/media/l0HlHSB8v5yRtBlHW/giphy.gif?cid=ecf05e47669fb7248d0aef46b7fc8c7c9629ddea550ac0dd&rid=giphy.gif&ct=g" height="300"/>
</p>

An Producer is an optional mixin type which modifies the constructed item of any of the Factory types before returning the created item. All Producer subclasses must have an `produce` method. Out-of-the-box, all `wonka` factories check to see if an Producer is mixed in before returning the completed project. `wonka` includes three basic types of closers:
* `Classer`: Always changes a factory's product to a class.
* `Flexer`: Conditions a factory's product type on whether a `parameters` argument is passed. If `parameters` are passed, an instance is always returned. Otherwise, the product is left as is.
* `Instancer`: Always changes a factory's product to an instance.

New closers may be added by simply subclassing `wonka.Producer`.

### Global Settings

<p align="center">
<img src="https://media1.giphy.com/media/1132uJKzZQc4ow/giphy.gif?cid=ecf05e47ef17dbfa5a3eeba4ac2af127db0205e7a1871b7b&rid=giphy.gif&ct=g" height="300"/>
</p>

`wonka` includes two convenience functions for changing two global settings that set naming conventions for registry keys and creation method names. Those methods and settings are:

* `set_keyer` may be used to change the global value of `_KEY_NAMER`, which controls the naming convention for registry dictionary keys in `wonka`. This is particularly important for `Subclasser`, which automatically creates keys based on a class' `__subclasses__` attribute. By default, `_KEY_NAMER' infers a snakecase name of any passed value.
* `set_method_namer` may be used to change the global value of the `_METHOD_NAMER`, which controls the naming convention for creation method names used in dispatcher factories. By default `_METHOD_NAMER` uses a prefix of 'from_' followed by the snakecase name of the type of the passed `source` argument. So, as the example above indicates, a class method named `from_path` is used for creating a `Settings` instance from a file path.

# Contributing

Contributors are always welcome and should find `wonka` easy to work with. The project is highly documented so that users and developers can make `wonka` work with their projects. It is designed for Python coders at all levels. Even beginners should be able to follow the readable code and internal documentation to understand how it works.

# Similar Projects

* [dataclass_factory](https://github.com/reagento/dataclass-factory): factory for dataclass production from other common data types.
* [factory_boy](https://github.com/FactoryBoy/factory_boy): tool for dynamically creating objects for unit testing in Python.
* [Model Bakery](https://github.com/model-bakers/model_bakery): object factory for Django.
* [Polyfactory](https://github.com/litestar-org/polyfactory): factory framework for mock data generation.
