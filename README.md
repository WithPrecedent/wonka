# wonka

<p align="center">
<img src="https://github.com/WithPrecedent/wonka/blob/main/docs/images/logo.png?raw=true" alt="logo" style="width:250px;"/>
</p>

| | |
| --- | --- |
| Version | [![PyPI Latest Release](https://img.shields.io/pypi/v/wonka.svg?style=for-the-badge&color=steelblue&label=PyPI&logo=PyPI&logoColor=yellow)](https://pypi.org/project/wonka/) [![GitHub Latest Release](https://img.shields.io/github/v/tag/WithPrecedent/wonka?style=for-the-badge&color=navy&label=GitHub&logo=github)](https://github.com/WithPrecedent/wonka/releases)
| Status | [![Build Status](https://img.shields.io/github/actions/workflow/status/WithPrecedent/wonka/ci.yml?branch=main&style=for-the-badge&color=cadetblue&label=Tests&logo=pytest)](https://github.com/WithPrecedent/wonka/actions/workflows/ci.yml?query=branch%3Amain) [![Development Status](https://img.shields.io/badge/Development-Active-seagreen?style=for-the-badge&logo=git)](https://www.repostatus.org/#active) [![Project Stability](https://img.shields.io/pypi/status/wonka?style=for-the-badge&logo=pypi&label=Stability&logoColor=yellow)](https://pypi.org/project/wonka/)
| Documentation | [![Hosted By](https://img.shields.io/badge/Hosted_by-Github_Pages-blue?style=for-the-badge&color=navy&logo=github)](https://WithPrecedent.github.io/wonka)
| Tools | [![Documentation](https://img.shields.io/badge/MkDocs-magenta?style=for-the-badge&color=deepskyblue&logo=markdown&labelColor=gray)](https://squidfunk.github.io/mkdocs-material/) [![Linter](https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/charliermarsh/Ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/Ruff) [![Dependency Manager](https://img.shields.io/badge/PDM-mediumpurple?style=for-the-badge&logo=pdm&labelColor=gray)](https://PDM.fming.dev) [![Pre-commit](https://img.shields.io/badge/pre--commit-darkolivegreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=gray)](https://github.com/TezRomacH/python-package-template/blob/master/.pre-commit-config.yaml) [![CI](https://img.shields.io/badge/GitHub_Actions-navy?style=for-the-badge&logo=githubactions&labelColor=gray&logoColor=white)](https://github.com/features/actions) [![Editor Settings](https://img.shields.io/badge/Editor_Config-paleturquoise?style=for-the-badge&logo=editorconfig&labelColor=gray)](https://editorconfig.org/) [![Repository Template](https://img.shields.io/badge/snickerdoodle-bisque?style=for-the-badge&logo=cookiecutter&labelColor=gray)](https://www.github.com/WithPrecedent/wonka) [![Dependency Maintainer](https://img.shields.io/badge/dependabot-navy?style=for-the-badge&logo=dependabot&logoColor=white&labelColor=gray)](https://github.com/dependabot)
| Compatibility | [![Compatible Python Versions](https://img.shields.io/pypi/pyversions/wonka?style=for-the-badge&color=steelblue&label=Python&logo=python&logoColor=yellow)](https://pypi.python.org/pypi/wonka/) [![Linux](https://img.shields.io/badge/Linux-lightseagreen?style=for-the-badge&logo=linux&labelColor=gray&logoColor=white)](https://www.linux.org/) [![MacOS](https://img.shields.io/badge/MacOS-snow?style=for-the-badge&logo=apple&labelColor=gray)](https://www.apple.com/macos/) [![Windows](https://img.shields.io/badge/Windows-blue?style=for-the-badge&logo=data:image/png;base64,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&labelColor=gray)](https://www.microsoft.com/en-us/windows?r=1)
| Stats | [![PyPI Download Rate (per month)](https://img.shields.io/pypi/dm/wonka?style=for-the-badge&color=steelblue&label=Downloads%20💾&logo=pypi&logoColor=yellow)](https://pypi.org/project/wonka) [![GitHub Stars](https://img.shields.io/github/stars/WithPrecedent/wonka?style=for-the-badge&color=navy&label=Stars%20⭐&logo=github)](https://github.com/WithPrecedent/wonka/stargazers) [![GitHub Contributors](https://img.shields.io/github/contributors/WithPrecedent/wonka?style=for-the-badge&color=navy&label=Contributors%20🙋&logo=github)](https://github.com/WithPrecedent/wonka/graphs/contributors) [![GitHub Issues](https://img.shields.io/github/issues/WithPrecedent/wonka?style=for-the-badge&color=navy&label=Issues%20📘&logo=github)](https://github.com/WithPrecedent/wonka/graphs/contributors) [![GitHub Forks](https://img.shields.io/github/forks/WithPrecedent/wonka?style=for-the-badge&color=navy&label=Forks%20🍴&logo=github)](https://github.com/WithPrecedent/wonka/forks)
| | |


## What is wonka?

`wonka`[^1] is an extensible library for simple class and
object constructors in Python. Out-of-the-box, `wonka` has implementations of
several common creational design patterns, including: registry factories,
prototypers, and composite builder workflows. It is also easy to extend `wonka`
by adding your own custom factories[^2] while taking advantage of `wonka`'s
convenient mixin classes and helper functions.

This readme offers a basic outline of how `wonka` works. If you would prefer to
jump right into the full documentation, go
[here](https://WithPrecedent.github.io/wonka).

## Why use wonka?

<p align="center">
<img src="https://media.giphy.com/media/y0SJVYxf90J1u/giphy.gif" alt="The suspense is terrible. I hope it'll last" style="width:300px;"/>
</p>

*“No other factory in the world mixes its chocolate by waterfall… But it’s the only way if you want it just right.”* - Willy Wonka

Factories are essential components of projects with dynamic, runtime implementation of different strategies. In Python packages, despite their commmon usage, factories are often poorly implemented, fragile, or inflexible. `wonka` addresses those common shortcomings by offering convenient creation through a simple, adaptable system that has almost no learning curve[^3]. `wonka` is:

* **Intuitive**: factories use a common interface with a `create` class method for all construction operations.
* **Extensible**: core classes can be adapted and extended through inheritance or composition.
* **Flexible**: whenever possible, factories can be mixed in for class and object self-creation or be used for creating external items.
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

There are three categories of base classes in `wonka`: factories, managers, and producers.

#### Factories

<p align="center">
<img src="https://media2.giphy.com/media/o4aGs2I3rVKjC/giphy.gif" alt="Come with me and you'll be in a world of pure imagination" style="width:350px;"/>
</p>

All `wonka` factory classes have a `create` class method which is used to construct new items. The only required argument for `create` is `item`, which contains the construction data.

Out-of-the-box, this library offers three general subtypes of its base `Factory` class. These are not subclasses, but rather describe the type of functionality in the included `Factory` subclasses.

* Registries - factories that build classes or objects from explicit or implicit registries.
* Dispatchers - factories that call appropriate creation methods or functions based on the type or content of data passed.
* Prototypers - factories that clone exsting classes or objects.

#### Managers

<p align="center">
<img src="https://media.giphy.com/media/NsBAHgohHByp2/giphy.gif" alt="Don't just stand there! Do something!" style="width:300px;"/>
</p>

For more complex construction, you can use subclasses of `Manager`, which is an iterable constructor. Every `Manager` subclass may construct items in three ways:

1. Calling its `manage` method.
2. Calling its `create` method (which just calls the `manage` method, but this allows a `Manager` subclass instance to be used anywhere a `Factory` could be used while still being distinguishable from an ordinary `Factory`).
3. Iterating it directly.

#### Producers

<p align="center">
<img src="https://media4.giphy.com/media/l0HlHSB8v5yRtBlHW/giphy.gif" alt="Willy Wonka completes a forward roll and pops up" style="width:350px;"/>
</p>

As another optional feature, `wonka` supports post-construction modification of built items through subclasses of `Producer`. This is particularly important for factories that use other resources (such as registries). `wonka` [separates concerns](https://dev.to/suspir0n/soc-separation-of-concerns-5ak7) so that the return value can be modified through a simple mixin system. This division of labor makes it incredibly easy to put together a `Factory` or `Manager` with a `Producer`.

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

## Acknowledgments

I would like to thank the University of Kansas School of Law for tolerating and
supporting this law professor's coding efforts, an endeavor which is well
outside the typical scholarly activities in the discipline.

Lastly, I want to extend a special thanks to the late, great Gene Wilder, whose
work inspired the name of this project and made my childhood better.

<p align="center">
<img src="https://media.giphy.com/media/3o6ZtbOoOHu28ftYiI/giphy.gif" alt="RIP, Gene Wilder, 1933-2016" style="width:200px;"/>
</p>

## License

Use of this repository is authorized under the [Apache Software License 2.0](https://www.github.com/WithPrecedent/wonka/blog/main/LICENSE).

[^1]: This project is not affiliated with Willy Wonka candy, either of the Willy Wonka films (especially the Johnny Depp one), or any other Willy Wonka product. It's just named "wonka" because all of the most obvious names for a Python package of factories and other constructors on [pypi.org](https://pypi.org) were taken and Willy Wonka's insane candy factory was the first relevant pop-culture touchstone I could think of.

[^2]: For the sake of brevity, the documentation refers to all of `wonka`'s constructors as "factories," even though many do not fit the definition of the classic [factory design pattern](https://realpython.com/factory-method-python/).

[^3]: Chocolate waterfalls are, sadly, only virtually implemented in `wonka`.