"""
test_storage: tests wonka constructor storage classes
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
   
    
"""
from __future__ import annotations
import dataclasses
from typing import Any, ClassVar

import wonka
from wonka.storage import Manufacturer


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
    depot = Manufacturer()
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
