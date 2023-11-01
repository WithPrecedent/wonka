# Tutorial

There are three categories of base classes in `wonka`: factories, managers, and
producers. Each is described in greater detail below.

## Factories

Out-of-the-box, this library offers three general subtypes of its base `Factory` class. These are not subclasses, but rather describe the kind of functionality in the included `Factory` subclasses.

* Registries - factories that build classes or objects from explicit or implicit registries.
* Dispatchers - factories that call appropriate creation methods or functions based on the type or content of data passed.
* Prototypers - factories that clone exsting classes or objects.

Here are the included factories:

| `Factory` | Subtype | Produces | Description |
| --- | --- | --- | --- |
| `Registrar` | Registry | Class or Instance | Creates items from data in `registry` |
| `Subclasser` | Registry | Subclass | Like `Registrar`, but without the `registry` attribute |
| `Sourcerer` | Dispatcher | Class or Instance | Calls the appropriate creation class method from data in `sources` |
| `Delegate` | Dispatcher | Class or Instance | Like `Sourcerer`, but without `sources` |
| `Scribe` | Prototyper | Class or Instance | Makes a deep copy of an item |

## Managers

These are the Manager classes included in `wonka`:

| `Manager` | Manages | Produces | Description |
| --- | --- | --- | --- |
| `Assembler` | `Factory` Classes, `Factory` Instances, and/or other `Manager` Instances | Class(es) and/or Instance(s) | A linear constructer, like an assembly line |

## Producers

These are the basic producers provied by `wonka`:

| `Producer` | Mixes With | Produces | Description |
| --- | --- | --- | --- |
| `Classer` | `Factory` or `Manager` | Class | `create` method always returns a class |
| `Flexer` | `Factory` or `Manager` | Class or Instance | `create` returns a class or instance, depending on data passed |
| `Instancer` | `Factory` or `Manager` | Instance | `create` method always returns an instance |
