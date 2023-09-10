""" Tests wonka construction managers."""

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


def test_assembler():
    assembly_line = wonka.Assembler()

    dictionary = {'verbose': True, 'processors': 8}
    config = Registration_Desk.create(
        'configuration',
        parameters = {'contents': dictionary})
    other_dictionary = {'ghost': 'town'}
    setup = Options.create(
        'configuration',
        parameters = {'contents': other_dictionary})
    assembly_line.add(config)
    assembly_line.add(setup)
    return

if __name__ == '__main__':
    test_assembler()
