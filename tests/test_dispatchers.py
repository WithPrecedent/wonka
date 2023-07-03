"""
test_dispatchers: tests wonka dispatcher factories
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
from collections.abc import MutableMapping
import dataclasses
from typing import Any, ClassVar

import camina
import pytest

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
    new_contents = camina.Dictionary(contents)
    new_configuration = Configuration.create(new_contents)
    assert new_configuration.contents['ghost'] == 'town'  
    assert isinstance(new_configuration, Configuration)  
    return


if __name__ == '__main__':
    test_delegate()
    test_sourcerer()
