"""
base: base classes for wonka factories
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
    Factory (abc.ABC): interface for basic wonka creation classes. A 'create' 
        class method is required for subclasses.
    Manager (Iterable, abc.ABC): iterable interface for complex construction 
        managers. A 'manage' instance method is required for subclasses. For
        compatibility as a wonka constructor, a 'create' property is included
        which automatically calls the 'manage' method with all args and kwargs.
    Producer (abc.ABC): mixin interface for classes that alter created items 
        before returning them. A 'produce' class method is required for 
        subclasses.
    Constructor (TypeAlias): type alias for a wonka.compatible constructor type.
        By default, it includes a Factory subclass, a Factory subclass instance,
        and a Manager subclass instance.

To Do:

        
"""
from __future__ import annotations
import abc
from collections.abc import Hashable, Iterable, MutableMapping
import dataclasses
from typing import Any, Optional, Type, TypeAlias

import camina


@dataclasses.dataclass
class Factory(abc.ABC):
    """Base for wonka constructors.
    
    A wonka Factory can be subclassed into any constructer design (not just 
    those that fit the classical "factory" design pattern). So, for example, the
    wonka package itself includes Factory subclasses that fit the prototype
    (Scribe), registry (Registar and Subclasser), and traditional (Delegate and
    Sourcerer) design patterns. Further, the Manager class may act as the
    director in a builder design pattern.
    
    One of the goals of wonka, though, is not be be wedded to or worried about
    the underlying design pattern. Instead, all constructers follow the simple,
    universal, and easily extensible interface of Factory. 
    
    If you want to add code that modifies output of a Factory's 'create' class
    method, you can either include that in the subclass 'create' method or by
    mixing in a Producer class. Details on how to use Producers are included in
    its documentation. Out-of-the-box, wonka includes three basic Producer
    subclasses which force the 'create' method to either always return a class
    (Classer), always return an instance (Instancer), or return a class or
    instance based on whether an argument is passed for 'parameters' to the 
    'create' method (Flexer).
    
    """

    """ Required Subclass Methods """

    @classmethod
    @abc.abstractmethod
    def create(cls, item: Any, *args: Any, **kwargs: Any) -> Any:
        """Returns a created or modified item.
        
        Args:
            item (Any): data for creation of an item or an item to be modified.     
                         
        Returns:
            Any: created or modified item.
                
        """
        pass


@dataclasses.dataclass
class Manager(Iterable, abc.ABC):
    """Base for manageing complex class or object construction.
    
    Args:
        contents (Iterable): an iterable containing Factory subclasses or
            Manager subclass instances.
                          
    """
    contents: Iterable
    
    """ Required Subclass Methods """
    
    @abc.abstractmethod
    def manage(self, item: Any, *args: Any, **kwargs: Any) -> Any:
        """Manages construction and/or modification based on 'item'.
        
        Args:
            item (Any): item to be passed to factories in 'contents'.
                         
        Returns:
            Any: constructed item.
                
        """
        pass

    """ Properties """

    @property
    def create(self, *args, **kwargs) -> Any:
        """Calls 'manage' method with args and kwargs.
        
        This property is included as a convenience so that an instance of a 
        Manager can be used as a drop-in for a Factory subclass. Manager cannot
        easily be made a subclass for Factory because it will often need to rely 
        on instance data for construction. So, every Manager subclass should be 
        designed such that an instance of that subclass could be substituted for 
        a Factory subclass. This allows other Manager subclass instances to be 
        stored in 'contents' as part of an iterable workflow.
        
        """
        return self.manage(*args, **kwargs)

    """ Dunder Methods """
    
    def __iter__(self) -> Iterable:
        """Returns iterable of 'contents'.
        
        Manager is agnostic as to the type of iterable that is used in order to
        accomodate simple sequences, complex graphs, nested trees, or any other
        workflow design. As a general practice, though, any mapping should 
        probably return 'items()' so that the interface for iteration never 
        requires any appended method call. But nothing in wonka precludes a
        different rule or practice.
        
        """
        return iter(self.contents)


@dataclasses.dataclass
class Producer(abc.ABC):
    """Base mixin for modifying items.
    
    A Producer's 'produce' method will automatically be called if it is mixed-in
    with any of the Factory classes in wonka. If you want a custom Factory
    subclass to similarly automatically check for a 'produce' method, the 
    easiest way to do that is to simply call the 'finalize' function as your 
    return value for the Factory's 'create' method as follows:
    
    return wonka.finalize(item = item, parameters = parameters)
    
    """
    
    """ Required Subclass Methods """
    
    @classmethod
    @abc.abstractmethod
    def produce(
        cls,
        item: Any,
        parameters: Optional[MutableMapping[Hashable, Any]] = None) -> Any:
        """Modifies 'item' and possibly incorporates 'parameters'.
        
        Args:
            item (Any): item to be modified. 
            parameters: Optional[MutableMapping[Hashable, Any]]: keyword 
                arguments to pass or add to a created instance. Defaults to 
                None.       
                         
        Returns:
            Any: modified item.
                
        """
        pass


Constructor: TypeAlias = Factory | Type[Factory] | Manager
  