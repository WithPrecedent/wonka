"""
prototypers: factory classes that clone items
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

Contents:  
    Scribe (base.Factory): factory that clones a passed argument or, if none is
        passed, itself.
                   
ToDo:


"""
from __future__ import annotations
from collections.abc import Hashable, MutableMapping
import copy
import dataclasses
from typing import Any, Optional

from . import base
from . import shared

        
@dataclasses.dataclass
class Scribe(base.Factory):
    """Base class for cloning classes or objects."""
    
    """ Class Methods """
    
    @classmethod
    def create(
        cls,
        item: Optional[Any] = None,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Clones 'item' and possibly incorporates 'parameters'.
        
        Args:
            item (Optional[Any]): item to clone. If it is None, the 'create' 
                method assumes that it should clone itself. Defaults to None.
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance. Defaults to 
                None.       
                         
        Returns:
            Any: cloned item.
                
        """
        item = item or cls
        item = copy.deepcopy(item)
        return shared.finalize(item = item, parameters = parameters)
        