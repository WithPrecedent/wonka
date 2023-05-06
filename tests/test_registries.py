"""
test_registries: tests wonka registry factories
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
