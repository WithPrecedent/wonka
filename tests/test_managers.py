"""
test_managers: tests wonka construction managers
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2023, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

ToDo:
   Test 'manage' method of Assembler
    
"""
from __future__ import annotations
import dataclasses
from typing import Any, ClassVar

import pytest

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
