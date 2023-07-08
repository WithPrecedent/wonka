""" Factory classes that clone items.

Contents:  
    Scribe (base.Factory): factory that clones a passed argument or, if none is
        passed, itself.
                   
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
        