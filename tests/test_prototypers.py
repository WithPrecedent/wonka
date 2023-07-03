"""
test_prototypers: tests wonka prototyper factories
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

import pytest

import wonka


@dataclasses.dataclass
class Clone(wonka.Scribe):
    
    contents: dict[str, wonka.Factory] = dataclasses.field(
        default_factory = lambda: {'tree': 'house', 'ghost': 'town'})
    

def test_scribe():
    clone_class = Clone.create()
    clone_instance = clone_class()
    assert clone_instance.contents['tree'] == 'house'
    assert isinstance(clone_instance, Clone)
    new_clone_instance = Clone.create(parameters = {})
    assert new_clone_instance.contents['ghost'] == 'town'
    assert isinstance(new_clone_instance, Clone)
    return

if __name__ == '__main__':
    test_scribe()

    