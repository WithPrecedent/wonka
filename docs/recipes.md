# Recipes

## `Sourcerer` Recipe for Accepting Different Data Types

This example is simplified adaptation from the
[`bobbie`](https://github.com/WithPrecedent/bobbie) configuration settings
repository. This code sets up a Settings class that will call a different
construction method depending on the type of data passed:

```python

import configparser
import dataclasses
import pathlib
from collections.abc import Callable, MutableMapping
from typing import Any, ClassVar
import yaml

import wonka

_FILE_EXTENSIONS: dict[str, str] = {
    'ini': 'ini',
    'yaml': 'yaml',
    'yml': 'yaml'}
_LOAD_METHOD: Callable[[str], str] = lambda x: f'from_{x}'

@dataclasses.dataclass
class Settings(wonka.Sourcerer):

    contents: MutableMapping[str, Any] = dataclasses.field(
        default_factory = dict)
    sources: ClassVar[MutableMapping[type[Any], str]] = {
        pathlib.Path: 'file',
        str: 'file',
        MutableMapping: 'dict'}

    @classmethod
    def from_dict(cls, source: MutableMapping[str, Any]) -> Settings:
        return cls(source)

    @classmethod
    def from_file(cls, source: str | pathlib.Path) -> Settings:
        if isinstance(source, str):
            source = pathlib.Path(item)
        if source.is_file():
            # Gets file extension and looks up the appropriate function to call.
            extension = source.suffix[1:]
            file_type = _FILE_EXTENSIONS[extension]
            name = _LOAD_METHOD(file_type)
            try:
                return getattr(cls, name)(source)
            except AttributeError as error:
                message = f'Loading from {file_type} file is not supported'
                raise TypeError(message) from error
        else:
            message = f'settings file {source} not found'
            raise FileNotFoundError(message)

    @classmethod
    def from_ini(cls, source: str | pathlib.Path) -> Settings:
        if isinstance(source, str):
            source = pathlib.Path(item)
        try:
            contents = configparser.ConfigParser()
            contents.optionxform = lambda option: option
            contents.read(source)
        except (KeyError, FileNotFoundError) as error:
            message = f'settings file {source} not found'
            raise FileNotFoundError(message) from error
        return cls(contents)

    @classmethod
    def from_yaml(cls, source: str | pathlib.Path) -> Settings:
        if isinstance(source, str):
            source = pathlib.Path(item)
        try:
            with open(source) as config:
                contents = yaml.safe_load(config)
        except FileNotFoundError as error:
            message = f'settings file {path} not found'
            raise FileNotFoundError(message) from error
        return cls(contents)

```

The `Settings` class inherits the `create` class method from `wonka.Sourcerer`.
So, the user just needs to pass a file or `dict` to the `create` classmethod and
it will return a `Settings`. So, if your settings are stored in an `ini` file,
you just used this code:

```python

settings = Settings.create('configuration.ini')

```

Or, if you have the settings in a Python `dict` named `configuration`, you just
do this:

```python

configuration = {
    'general': {
        'verbose': True,
        'seed': 43},
    'tasks': {
        'things_to_do': ['stop', 'drop', 'roll']},
    'tasks_parameters': {
        'start': 'when_ready',
        'end': 'when_done'}}

settings = Settings.create(configuration)

```