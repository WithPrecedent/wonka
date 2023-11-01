""" Tests wonka dispatcher factories. """

from __future__ import annotations
from collections.abc import MutableMapping
import dataclasses
from typing import Any, ClassVar

import wonka


@dataclasses.dataclass
class Settings(wonka.Delegate):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Settings:
        return cls(contents = item)


@dataclasses.dataclass
class Configuration(wonka.Sourcerer):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)
    sources: ClassVar[dict[str, Any]] = {MutableMapping: 'dictionary'}

    @classmethod
    def from_dictionary(cls, item: dict[str, Any]) -> Configuration:
        return cls(contents = item)


def test_delegate():
    contents = {'tree': 'house', 'ghost': 'town'}
    settings = Settings.create(contents)
    assert settings.contents['tree'] == 'house'
    assert isinstance(settings, Settings)
    return

def test_sourcerer():
    contents = {'tree': 'house', 'ghost': 'town'}
    configuration = Configuration.create(contents)
    assert configuration.contents['tree'] == 'house'
    assert isinstance(configuration, Configuration)
    new_configuration = Configuration.create(contents)
    assert new_configuration.contents['ghost'] == 'town'
    assert isinstance(new_configuration, Configuration)
    return


if __name__ == '__main__':
    test_delegate()
    test_sourcerer()
