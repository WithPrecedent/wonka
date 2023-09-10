""" Test_producers: tests wonka producer mixins.

ToDo:
    Use better example to test Flexer (which isn't working right now because of
        the use of Delegate classes in the tests)

"""
from __future__ import annotations
import dataclasses
import inspect
from typing import Any

import wonka


@dataclasses.dataclass
class Configuration(wonka.Classer, wonka.Delegate):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Settings:
        return cls(contents = item)


@dataclasses.dataclass
class Settings(wonka.Flexer, wonka.Delegate):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Settings:
        return cls(contents = item)


@dataclasses.dataclass
class Setup(wonka.Instancer, wonka.Delegate):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> Settings:
        return cls(contents = item)


def test_classer():
    contents = {'tree': 'house', 'ghost': 'town'}
    config = Configuration.create(contents)
    assert inspect.isclass(config)
    return

def test_flexer():
    contents = {'tree': 'house', 'ghost': 'town'}
    config = Settings.create(contents)
    assert not inspect.isclass(config)
    return

def test_instancer():
    contents = {'tree': 'house', 'ghost': 'town'}
    config = Setup.create(contents)
    assert not inspect.isclass(config)
    return


if __name__ == '__main__':
    test_classer()
    test_flexer()
    test_instancer()
