"""
test_producers: tests wonka producer mixins
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
    Use better example to test Flexer (which isn't working right now because of
        the use of Delegate classes in the tests)
  
"""
from __future__ import annotations
from collections.abc import Hashable, MutableMapping
import dataclasses
import inspect
from typing import Any, ClassVar, Optional, Type

import pytest

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

    