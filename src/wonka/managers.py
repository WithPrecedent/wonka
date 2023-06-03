"""
managers: manager classes for iterable constructors
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
    Assembler (camina.Listing, base.Manager): iterable that stores a list of
        constructors that build an item like an assembly line.
               
ToDo:


"""
from __future__ import annotations
from collections.abc import Hashable, MutableSequence, Sequence
import dataclasses
from typing import Any, ClassVar, Optional, Type

import camina

from . import base
from . import shared

        
@dataclasses.dataclass
class Assembler(camina.Listing, base.Manager):
    """Assembly line constructer. 
    
    Assembler stores a sequence of wonka constructors that are called by the
    'manage' (or 'create') method in order to construct an item.
    
    Args:
        contents (MutableMapping[Hashable, base.Factory]): stored constructors.
            Defaults to an empty list.
                          
    """
    contents: MutableSequence[base.Constructor] = dataclasses.field(
        default_factory = list)
     
    """ Instance Methods """
     
    def add(self, item: base.Constructor | Sequence[base.Constructor]) -> None:
        """Adds 'item' to the 'contents' attribute.
        
        Args:
            item (base.Constructor | Sequence[base.Constructor]): item(s) to add 
                to 'contents' attribute.
        
        Raises:
            TypeError: if all of the values of 'item' are not wonka-compatible
                constructors.
                
        """
        if shared.is_constructor(item):
            self.contents.append(item)
        elif (isinstance(item, Sequence) 
                and all(shared.is_constructor(v) for v in item)):
            self.contents.extend(item)
        else:
            raise TypeError(
                'All values in item must be wonka-compatible constructors')
        return

    def manage(self, item: Any) -> Any:
        """Manages construction and/or modification based on 'item'.
        
        Args:
            item (Any): item to be passed to constructors in 'contents'.
                         
        Returns:
            Any: constructed item.
                
        """
        for constructor in self.contents:
            item = constructor.create(item)
        return item
  