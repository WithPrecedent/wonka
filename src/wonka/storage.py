""" Stores groups of wonka constructors.

Contents:  
    Manufacturer (camina.Dictionary): dict-like class that stores wonka 
        constructors. Has an 'add' method while validates any added values as 
        wonka compatible.
                 
"""
from __future__ import annotations
from collections.abc import Hashable, MutableMapping
import dataclasses
from typing import Any, Optional

import camina

from . import base
from . import configuration
from . import shared

 
@dataclasses.dataclass
class Manufacturer(camina.Dictionary):
    """Dictionary of factories.

    A Manufacturer may serve as a one-stop spot for constructors. Each 
    constructor need not be of the same subtype, as they pass the 
    'is_constructor' test. The use of a Manufacturer is wholly optional - it is 
    just a convenience offered by wonka. To access individual constructors, the 
    following format should be used:
    
    manufacturer_instance['constructor_name'].create(*args, **kwargs)
    
    Args:
        contents (MutableMapping[Hashable, base.Constructor]): stored dict of
            wonka constructors. Defaults to an empty dict.
        default_factory (Optional[Any]): default value to return or default 
            callable to use to create the default value.
                          
    """
    contents: MutableMapping[Hashable, base.Constructor] = dataclasses.field(
        default_factory = dict)
    default_factory: Optional[Any] = None
     
    """ Instance Methods """
     
    def add(
        self, 
        item: MutableMapping[
            Hashable, base.Constructor] | base.Constructor) -> None:
        """Adds 'item' to the 'contents' attribute.
        
        Args:
            item (MutableMapping[Hashable, Any] | base.Constructor): item(s) to 
                add to 'contents' attribute.
        
        Raises:
            TypeError: if all of the values of 'item' are not wonka-compatible 
                constructors or if 'item' itself is not a wonka-compatible 
                constructor.
                
        """
        if isinstance(item, MutableMapping):
            if all(shared.is_constructor(v) for v in item.values()):
                self.contents.update(item)
            else:
                raise TypeError(
                    'All values in item must be wonka-compatible constructors')
        elif shared.is_constructor(item):
            key = configuration._KEY_NAMER(item)
            self.contents.update({key: item})
        else:
            raise TypeError(
                'item must either be a wonka-compatible constructor or a dict-'
                'like object with values that are constructors')
        return
   