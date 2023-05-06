"""
producers: mixins for created objection modification
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
    Classer (base.Producer, abc.ABC): Producer with an 'produce' method that 
        always returns a class.
    Flexer (base.Producer, abc.ABC): Producer that conditions return value of 
        the 'produce' method based on whether 'parameters' are passed.
    Instancer (base.Producer, abc.ABC): Producer with an 'produce' method that 
        always returns an instance.   
                   
ToDo:


"""
from __future__ import annotations
import abc
from collections.abc import Hashable, MutableMapping
import dataclasses
import inspect
from typing import Any, ClassVar, Optional, Type

from . import base
from . import shared


@dataclasses.dataclass
class Classer(base.Producer, abc.ABC):
    """Producer with an 'produce' method always return a class."""
    
    """ Class Methods """
    
    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Modifies 'item' and possibly incorporates 'parameters'.
        
        Args:
            item (Any): item created by a constructor that may need to be 
                altered before being returned by the constructor 'create' 
                method. 
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance. Defaults to 
                None. The argument for 'parameters' is ignored by Classer - it
                is only included to provide a consistent interface across all
                Producer subclasses.      
                         
        Returns:
            Any: modified item.
                
        """
        return item if inspect.isclass(item) else item.__class__


@dataclasses.dataclass
class Flexer(base.Producer, abc.ABC):
    """Producer that conditions return value of the 'produce' method.
    
    If 'parameters' are passed to the 'produce' method, an instance is always
    returned. If no 'parameters' are passed, the item will be returned as-is
    (depending on the constructor used).
    
    """
    
    """ Class Methods """
    
    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Modifies 'item' and possibly incorporates 'parameters'.
        
        Args:
            item (Any): item created by a constructor that may need to be 
                altered before being returned by the constructor 'create' 
                method. 
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance. Defaults to 
                None.       
                         
        Returns:
            Any: modified item.
                
        """
        if parameters is None:
            return item  
        elif inspect.isclass(item):
            return item(**parameters)
        else:
            return shared.inject_attributes(item, parameters)


@dataclasses.dataclass
class Instancer(base.Producer, abc.ABC):
    """Producer with an 'produce' method always return an instance."""
    
    """ Class Methods """
    
    @classmethod
    def produce(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Modifies 'item' and incorporates 'parameters'.
        
        Args:
            item (Any): item created by a constructor that may need to be 
                altered before being returned by the constructor 'create' 
                method. 
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance. Defaults to 
                None.       
                         
        Returns:
            Any: modified item.
                
        """
        if inspect.isclass(item) and parameters is None:
            return item()
        elif parameters is None:
            return item  
        elif inspect.isclass(item):
            return item(**parameters)
        else:
            return shared.inject_attributes(item, parameters)
