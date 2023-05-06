"""
core: business logic functions for wonka
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
    finalize: finalizes construction before returning a value, including calling
        the 'produce' method of the passed item.
    inject_attributes: adds keys and values of a mapping to a class or instance
        as attributes.
    is_constructor: returns boolean as to whether an item is a wonka-compatible
        constructor.
            
ToDo:


"""
from __future__ import annotations
from collections.abc import Hashable, Mapping, MutableMapping, MutableSequence
import inspect
from typing import Any, Callable, ClassVar, Optional, Type, TypeAlias

from . import base
from . import configuration


def finalize(
    item: Any, 
    parameters: Optional[MutableMapping[Hashable, Any]] = None,
    factory: Optional[Type[base.Factory]] = None) -> Any:
    """Modifies 'item' and possibly incorporates 'parameters'.
        
    Args:
        item (Any): item created by a factory that may need to be altered
            before being returned by the factory 'create' method. 
        parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
            arguments to pass or add to a created instance. Defaults to 
            None.   
        factory (Optional[Type[base.Factory]]): the factory used to create
            'item'. This need not be passed if 'item' is also the factory for
            its creation. Defaults to None. If 'factory' is None, this function
            will look for an 'produce' method on item.
    
    Returns:
        Any: modified item.
           
    """
    factory = factory or item
    if (hasattr(factory, 'produce') 
            and inspect.ismethod(getattr(factory, 'produce'))):
        return factory.produce(item, parameters)
    else:
        return item if parameters is None else item(**parameters)

def inject_attributes(
    item: Any,
    parameters: Optional[MutableMapping[Hashable, Any]] = None,
    overwrite: Optional[bool] = None) -> Any:
    """Manages 'item' and possibly incorporates 'parameters'.
    
    Args:
        item (Any): item to have 'parameters' injected.
        parameters: Optional[MutableMapping[Hashable, Any]]: keyword arguments 
            to add to a created instance. Defaults to None. 
        overwrite (Optional[bool]): whether to overwrite existing attributes,
            if they exist. Defaults to None. If the value is None, the global
            _OVERWRITE setting will be used.      
                        
    Returns:
        Any: modified item.
            
    """
    if parameters:
        overwrite = configuration._OVERWRITE if overwrite is None else overwrite
        for key, value in parameters.items():
            if overwrite or not hasattr(item, key):
                setattr(item, key, value)
    return item

def is_constructor(item: Any) -> bool:
    """Returns if 'item' is a wonka-compatible constructor.
    
    If the global '_STRICT_COMPATIBILITY' setting is True, this function uses a 
    narrow definition of 'constructor' to only include:
        1) subclasses or instances of Factory; or
        2) subclasss instances of Manager.
    If '_STRICT_COMPATIBILITY' is False, the function merely tests whether 
    'item' has a 'create' method.

    Args:
        item (Any): item to test

    Returns:
        bool: whether 'item' is a wonka-compatible constructor
        
    """
    if configuration._STRICT_COMPATIBILITY:
        return (
            (inspect.isclass(item) and issubclass(item, base.Factory))
            or isinstance(item, base.Manager | base.Factory))
    else:
        return (
            hasattr(item, 'create') 
            and inspect.ismethod(getattr(item, 'create')))