"""
dispatchers: factory classes that call other construction methods or functions
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
    Delegate (base.Factory): builds classes and/or instances using methods 
        that follow a naming convention and the str names of the types of the
        first argument passed to the 'create' class method.  
    Sourcerer (base.Factory): builds classes and/or instances using methods 
        that follow a naming convention (set at 'configuration._METHOD_NAMER') 
        and a dict of types stored in the 'sources' class attribute.
          
ToDo:


"""
from __future__ import annotations
import abc
from collections.abc import Hashable, MutableMapping
import dataclasses
import inspect
from typing import Any, Callable, ClassVar, Optional, Type

from . import base
from . import configuration
from . import shared

                    
@dataclasses.dataclass
class Delegate(base.Factory):
    """Builds based on the str name of the type passed.

    This factory acts as a dispatcher to call other methods based on the type
    or name of the type passed in a manner identical to Sourcerer. However,
    unlike Sourcerer, Delegate only finds a matching creation method if the str 
    name of the type of 'item' matches a substring of the creation method name 
    using the format of 'configuration._METHOD_NAMER'
    
    """
    
    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Creates an item based on 'item' and possibly 'parameters'.
        
        Args:
            item (Any): data for construction of the returned item.       
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance.
                        
        Raises:
            AttributeError: If an appropriate method does not exist for the
                data type of 'item.'
            KeyError: If a corresponding subclass does not exist for 'item.'
                                                     
        Returns:
            Any: created item.
                
        """
        builder = _get_creation_method_name(item)
        item = _get_from_builder_method(
            factory = cls, 
            method = builder,
            source = item,
            **kwargs)
        return shared.finalize(item = item, parameters = parameters)

   
@dataclasses.dataclass
class Sourcerer(base.Factory, abc.ABC):
    """Builds based on compatibility with keys in the 'sources' class attribute.

    This factory acts as a dispatcher to call other methods based on the type
    passed. Unlike Delegate, Sourcerer is more forgiving by allowing the type 
    passed to a subtype or instance of the type listed as a key in the 'sources' 
    class attribute.
    
    The name for a Sourcerer is spelled the way it is instead of "Sorcerer" 
    because the 'sources' attribute is used. This is inspired by the Divinity:
    Original Sin games where the magic users are called "Sourcerers" because
    they may manipulate the magical energy known as "source". 
    https://divinity.fandom.com/wiki/Sourcerer
    
    Attributes:
        sources (ClassVar[MutableMapping[Type[Any], str]]): dict with keys that
            are types and values are substrings of the names of methods to call
            when the key type is passed to the 'create' method. Defaults to an
            empty dict.
    
    """
    sources: ClassVar[MutableMapping[Type[Any], str]] = dict()
    
    """ Class Methods """

    @classmethod
    def create(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None,
        **kwargs: Any) -> Any:
        """Creates an item based on 'item' and possibly 'parameters'.

        Args:
            item (Any): data for construction of the returned item.       
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance.
                        
        Raises:
            AttributeError: if the value matching the key 'item' does not
                correspond to a method in the Sourcerer subclass.
            KeyError: if there is no key in 'sources' matching the type for
                'item'.
                                                     
        Returns:
            Any: created item.
                
        """
        for kind, substring in cls.sources.items():
            if _is_kind(item, kind):
                builder = _get_creation_method_name(substring)
                item = _get_from_builder_method(
                    factory = cls, 
                    method = builder,
                    source = item,
                    **kwargs)
                return shared.finalize(item = item, parameters = parameters)
        raise KeyError(f'{item} does not match any recognized types')


def _get_creation_method_name(
    source: Any,
    method_namer: Optional[Callable[[object | Type[Any]], str]] = None) -> str:
    """Returns the creation method name for factories that call other methods.

    Args:
        source (Any): source data for creating a method name.
        method_namer (Optional[Callable[[object | Type[Any]], str]], optional): 
            callable to create the creation method name. Defaults to None. If it 
            is None, the global namer stored in configuration._METHOD_NAMER will 
            be used.

    Returns:
        str: name of the creation method to use.
        
    """
    if not isinstance(source, str):
        source = configuration._KEY_NAMER(source)
    namer = method_namer or configuration._METHOD_NAMER
    return namer(source)

def _is_kind(item: Any, kind: Type[Any]) -> bool:
    """Returns if 'item' is an instance or subclass of 'kind'.

    Args:
        item (Any): item to evalute.
        kind (Type[Any]): type to compare 'item' to.

    Returns:
        bool: whether 'item' is an instance or subclass of 'kind'.
        
    """
    return (
        isinstance(item, kind) 
        or (inspect.isclass(item and issubclass(item, kind))))

def _get_from_builder_method(
    factory: Any, 
    method: str, 
    source: Any, 
    **kwargs: Any) -> Any:    
    """Returns constructed item from a builder method of 'factory'.
    
    Args:
        factory (Any): factory class or instance.
        method (str): name of the method of factory to use to construct an item.
        source (Any): the source data used to create item.
        
    Raises:
        AttributeError: if 'factory' has no method named 'method'.
        
    Returns:
        Any: constructed item.
        
    """           
    try:
        builder = getattr(factory, method)
        return builder(source, **kwargs)
    except AttributeError as e:
        raise AttributeError(f'{method} does not exist in {factory}') from e
  