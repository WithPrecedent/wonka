""" Tests wonka registry factories. """
from __future__ import annotations
import dataclasses
from typing import Any, ClassVar

import wonka


@dataclasses.dataclass
class Options(wonka.Subclasser):
    pass


@dataclasses.dataclass
class Settings(Options):
    pass


@dataclasses.dataclass
class Configuration(Settings):

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)


@dataclasses.dataclass
class Setup(Settings):
    pass


@dataclasses.dataclass
class Registration_Desk(wonka.Registrar):

    registry: ClassVar[dict[str, Any]] = {
        'configuration': Configuration,
        'setup': Setup}


def test_registrar():
    dictionary = {'verbose': True, 'processors': 8}
    config = Registration_Desk.create(
        'configuration',
        parameters = {'contents': dictionary})
    assert config.contents['processors'] == 8
    assert isinstance(config, Configuration)
    return

def test_subclasser():
    dictionary = {'verbose': True, 'processors': 8}
    setup = Options.create(
        'configuration',
        parameters = {'contents': dictionary})
    assert setup.contents['processors'] == 8
    assert isinstance(setup, Configuration)
    return

if __name__ == '__main__':
    test_registrar()
    test_subclasser()
