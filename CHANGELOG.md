# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

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
