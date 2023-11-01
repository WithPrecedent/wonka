""" Tests wonka constructor storage classes. """
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


def test_manufacturer():
    dictionary = {'verbose': True, 'processors': 8}
    other_dictionary = {'tree': 'house', 'ghost': 'town'}
    depot = wonka.Manufacturer()
    depot.add(Options)
    depot.add({'registration': Registration_Desk})
    setup = depot['options'].create(
        'configuration',
        parameters = {'contents': dictionary})
    assert setup.contents['processors'] == 8
    assert isinstance(setup, Configuration)
    registration = depot['registration'].create(
        'configuration',
        parameters = {'contents': other_dictionary})
    assert registration.contents['tree'] == 'house'
    assert isinstance(registration, Configuration)
    return

if __name__ == '__main__':
    test_manufacturer()
