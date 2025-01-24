# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

## 0.2.0 (forthcoming)

* Added example to README.md
* Added more recipes to recipes.md
* Added Registry class, offering extra functionality beyond a `dict`
* Added documentation to advanced.md
* Added support for Python 3.13
* Changed 'Manager' 'create' property to a proper alias method for 'manage' to preserve its signature when introspected

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
