# wonka

<p align="center">
<img src="https://github.com/WithPrecedent/wonka/blob/main/docs/img/top_hat.png" alt="wonka top hat logo" style="width:250px;"/>
</p>

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/wonka.svg?style=for-the-badge&label=pypi&logo=PyPI&color=darkorange)](https://pypi.org/project/wonka/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/wonka?style=for-the-badge&label=branch&logo=github&color=navy)](https://github.com/WithPrecedent/wonka/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/wonka/ci.yml?branch=main&label=tests&style=for-the-badge&logo=pytest&color=cadetblue)](https://github.com/WithPrecedent/wonka/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-Green?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/badge/stability-beta-firebrick?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge&logo=apache&color=goldenrod)](https://opensource.org/licenses/Apache-2.0)
| Docs | [![Hosted By](https://img.shields.io/badge/hosted_by-github_pages-blue?style=for-the-badge&logo=github&color=navy)](https://WithPrecedent.github.io/wonka)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/wonka?style=for-the-badge&logo=python&color=darkorange)](https://pypi.python.org/pypi/wonka/) [![Linux](https://img.shields.io/badge/linux-maroon?style=for-the-badge&logo=linux&labelColor=gray)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/macos-yellow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/windows-blue?style=for-the-badge&logo=windows&labelColor=gray)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/wonka?style=for-the-badge&logo=pypi&color=darkorange)](https://pypi.org/project/wonka) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/wonka?style=for-the-badge&label=contributors&logo=github&color=darksalmon)](https://github.com/WithPrecedent/wonka/graphs/contributors) [![GitHub Contributors](https://img.shields.io/github/issues/WithPrecedent/wonka?style=for-the-badge&label=issues&logo=github&color=deeppink)](https://github.com/WithPrecedent/wonka/graphs/contributors) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/wonka?style=for-the-badge&label=Stars&logo=github&color=firebrick)](https://github.com/WithPrecedent/wonka/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/wonka?style=for-the-badge&label=forks&logo=github&color=coral)](https://github.com/WithPrecedent/wonka/forks)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/PDM-blueviolet?style=for-the-badge&logo=affinity&labelColor=gray)](https://PDM.fming.dev) [![Pre-commit](https://img.shields.io/badge/pre--commit-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/github_actions-yellow?style=for-the-badge&logo=githubactions&labelColor=gray)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/editor_config-blue?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://github.com/features/actions) [![Template](https://img.shields.io/badge/snickerdoodle-brown?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/snickerdoodle)
| | |

-----

## What is wonka?

`wonka`[^1] is an extensible library for simple implementation of class and object constructors in Python. Out-of-the-box, `wonka` has implementations of several common creational design patterns, including: registry factories, prototypers, and composite builder workflows. It is also easy to extend `wonka` by adding your own custom factories[^2] while taking advantage of `wonka`'s convenient mixin classes and helper functions. This readme file offers a basic outline of how `wonka` works. If you would prefer to jump right into the full documentation, go [here](https://WithPrecedent.github.io/wonka).

## Why use wonka?

<p align="center">
<img src="https://media.giphy.com/media/y0SJVYxf90J1u/giphy.gif" alt="The suspense is terrible. I hope it'll last" style="width:300px;"/>
</p>

*“No other factory in the world mixes its chocolate by waterfall… But it’s the only way if you want it just right.”* - Willy Wonka

Factories are essential components of coding projects that require dynamic, runtime implementation of different strategies or options. In Python packages, despite their commmon usage, factories are often poorly implemented, fragile, or inflexible. `wonka` addresses those common shortcomings by offering convenient creation through a simple, adaptable system that has almost no learning curve[^3]. `wonka` is:

* **Intuitive**: factories use a common interface with a `create` class method for all construction operations.
* **Extensible**: core classes can be adapted and extended through inheritance or composition.
* **Flexible**: whenever possible, factories can be mixed in for class and object self-creation or be used for creating external items.
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

There are three categories of base classes in `wonka`: factories, managers, and producers. Each is described in greater detail below.

### Factories

<p align="center">
<img src="https://media2.giphy.com/media/o4aGs2I3rVKjC/giphy.gif" alt="Come with me and you'll be in a world of pure imagination" style="width:350px;"/>
</p>

All `wonka` factory classes have a `create` class method which is used to construct new items. The only required parameter for `create` is `item`, which contains the data for building products. 

Out-of-the-box, this library offers three general subtypes of its base `Factory` class. These are not subclasses, but rather describe the type of functionality in the included `Factory` subclasses.

* Registries - factories that build classes or objects from explicit or implicit registries.
* Dispatchers - factories that call appropriate creation methods or functions based on the type or content of data passed.
* Prototypers - factories that clone exsting classes or objects.

Here are the included factories:

| Factory | Subtype | Produces | Description |
| --- | --- | --- | --- |
| Registrar | Registry | Class or Instance | Creates items from data in `registry` |
| Subclasser | Registry | Subclass | Like `Registrar`, but without the `registry` attribute |
| Sourcerer | Dispatcher | Class or Instance | Calls the appropriate creation class method from data in `sources` |
| Delegate | Dispatcher | Class or Instance | Like `Sourcerer`, but without `sources` |
| Scribe | Prototyper | Class or Instance | Makes a deep copy of an item |

### Managers

<p align="center">
<img src="https://media.giphy.com/media/NsBAHgohHByp2/giphy.gif" alt="Don't just stand there! Do something!" style="width:300px;"/>
</p>

For more complex construction, you can use subclasses of `Manager`, which is an iterable constructor. Every `Manager` subclass may construct items in three ways:

1. Calling its `manage` method.
2. Calling its `create` method (which just calls the `manage` method, but this allows a `Manager` subclass instance to be used anywhere a `Factory` could be used while still being distinguishable from an ordinary `Factory`).
3. Iterating it directly.

Here are the Manager classes included in `wonka`:

| Manager | Manages | Produces | Description |
| --- | --- | --- | --- |
| Assembler | Factory Classes, Factory Instances, and/or other Manager Instances | Class(es) and/or Instance(s) | A linear constructer, like an assembly line |

### Producers

<p align="center">
<img src="https://media4.giphy.com/media/l0HlHSB8v5yRtBlHW/giphy.gif" alt="Willy Wonka completes a forward roll and pops up" style="width:350px;"/>
</p>

As another optional feature, `wonka` supports post-construction modification of built items through subclasses of `Producer`. This is particularly important for factories that use other resources (such as registries). `wonka` [separates concerns](https://dev.to/suspir0n/soc-separation-of-concerns-5ak7) so that the return value can be modified through a simple mixin system. This division of labor makes it incredibly easy to put together a `Factory` or `Manager` with a `Producer`.

These are the basic producers provied by `wonka`:

| Producer | Mixes With | Produces | Description |
| --- | --- | --- | --- |
| Classer | Factory or Manager | Class | `create` method always returns a class |
| Flexer | Factory or Manager | Class or Instance | `create` returns a class or instance, depending on data passed |
| Instancer | Factory or Manager | Instance | `create` method always returns an instance |

## Contributing

Contributors are always welcome. Feel free to grab an [issue](https://www.github.com/WithPrecedent/wonka/issues) to work on or make a suggested improvement. If you wish to contribute, please read the [Contribution Guide](https://www.github.com/WithPrecedent/wonka/contributing.md) and [Code of Conduct](https://www.github.com/WithPrecedent/wonka/code_of_conduct.md).

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

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/wonka/blog/main/LICENSE).

[^1]: This project is not affiliated with Willy Wonka candy, either of the Willy Wonka films (especially the Johnny Depp one), or any other Willy Wonka product. It's just named "wonka" because all of the most obvious names for a Python package of factories and other constructors on [pypi.org](https://pypi.org) were taken and Willy Wonka's insane candy factory was the first relevant pop-culture touchstone I could think of.

[^2]: For the sake of brevity, the documentation refers to all of `wonka`'s constructors as "factories," even though many do not fit the definition of the classic [factory design pattern](https://realpython.com/factory-method-python/).

[^3]: Chocolate waterfalls are, sadly, only virtually implemented in `wonka`.
