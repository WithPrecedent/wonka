# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

## 0.3.0

* **Breaking:** `cluster + other` and `assembler + other` now return a new instance and leave both operands unchanged. Use `+=` to add `other` in place (the old behavior of "+").
* **Breaking:** `Assembler` now validates every constructor added with `insert`, `append`, `extend`, `prepend`, or item assignment, and raises a `TypeError` for anything that is not a wonka-compatible constructor. Before, only `add` validated.
* Added the `py.typed` marker so that type checkers use the type hints in `wonka`.
* Added a `subset` method to `Manufacturer`.
* Added slice support to `Assembler` indexing, assignment, and deletion.
* Added the `Parameters` type alias for the `parameters` argument (a mapping with `str` keys).
* Fixed `Assembler.prepend`, which added the contents of an `Assembler` instead of the `Assembler` itself.
* Fixed `Registrar.create`, which did not accept the keyword arguments that every `Factory.create` accepts.
* Fixed `Subclasser` choosing between subclasses with the same name in a random order. Subclasses are now found in a fixed, depth-first order without duplicates.
* Fixed the undefined names in the `Sourcerer` recipe.
* Removed the unfinished and broken `Hub` and `Keystone` classes, which were not exported or documented.
* Removed the unused `_is_sequence` and `_return_subset` utilities, the duplicate `_iterify`, the unused `GenericList`, `GenericSet`, and `SubsetReturns` aliases, and the commented-out code.
* Updated to the `snickerdoodle` 0.5.0 template (Codecov coverage, a coverage page in the docs, `pydoclint`, Python 3.15, SPDX license metadata, a version read from `__version__`, GitHub CLI releases, and `uv` updates from Dependabot). Added `.cruft.json` so that `cruft update` can apply future template changes.
* Removed the leftovers from `pdm` (the credits page and the script that read `pdm.lock`) and moved the issue templates out of a nested `ISSUE_TEMPLATE` folder.
* Restyled the package (spaces around keyword argument `=`, closing brackets on the last line, section markers, and complete docstrings). Ruff now enforces single quotes and the 80 character line limit, and ignores the `tests` folder when run by pre-commit.
* `mypy` now passes (there were 39 errors) and runs in CI.
* Reorganized the tests by module, added a fixture that restores the global options after each test, and added tests for the operators, slices, validation, `subset`, the dispatchers, the options, and the package metadata (100 tests in total, with 99% coverage).

## 0.2.2

* Updated to the `snickerdoodle` 0.4.0 template
* Removed `ruff format` from the `pre-commit` hooks because it removes the spaces around "=" in keyword arguments
* Made `ruff` prefer single quotes and converted the strings in the code to single quotes
* Made `ruff` ignore boolean default positional arguments (`FBT002`)
* Excluded `uv.lock` from the large file check
* Fixed typos in the contributing guide and noted that the project does not use a code formatter
* Fixed the LICENSE link in the README

## 0.2.1

* Added 'AutoRegistrar' and 'Cluster' to the package namespace and '__all__'
* Added tests for 'AutoRegistrar', edge cases, options, utilities, 'Assembler', 'Manufacturer', and producers
* Changed 'AutoRegistrar' so that each direct subclass gets its own registry instead of all families sharing one
* Changed 'Assembler' 'manage' to accept keyword arguments and pass them to each constructor
* Changed 'finalize' to inject parameters as attributes when the item is an instance, instead of calling it
* Changed 'Kwargs' type alias to 'Any' and applied it consistently to '**kwargs' annotations
* Changed '__delitem__' on 'Cluster' and 'Assembler' to return 'None'
* Fixed 'Sourcerer' raising 'TypeError' when an item did not match an earlier key in 'sources'
* Fixed dispatchers masking 'AttributeError' raised inside a builder method as a missing method
* Fixed 'Scribe' cloning itself instead of the item when the item was falsy

## 0.2.0

* Added example to README.md
* Added more recipes to recipes.md
* Added Registry class, offering extra functionality beyond a `dict`
* Added documentation to advanced.md
* Added support for Python 3.13
* Changed 'Manager' 'create' property to a proper alias method for 'manage' to preserve its signature when introspected
* Switched dependency manager to uv

## 0.1.5

* Fixed default for 'Registrar' registry class attribute
* Fixed wordwrap issue in tables in tutorial
* Added recipe to recipes.md
* Removed non-public classes and functions from documentation
* Fixed bug with Manager's `create` property so that it properly calls the
  `manage` method
* Changed required Python version to 3.11 or greater

## 0.1.4

* Removed empty keystons module until it is ready to prevent linting errors
* Updated out-of-date actions
* Removed extraneous actions

## 0.1.3

* Fixed unit test setting bug

## 0.1.2

* Transitioned to 0.1.9 `snickerdoodle` template
* Removed all external dependencies

## 0.1.1

* Added unit tests
* Added advanced documentation and full tutorial

## 0.1.0

* Initial commit
