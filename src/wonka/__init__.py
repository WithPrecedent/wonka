# wonka: runtime class and object creation, made simple
# Corey Rayburn Yung <coreyrayburnyung@gmail.com>
# Copyright 2023, Corey Rayburn Yung
# License: Apache-2.0
    
# ToDo:
#     Increase test coverage
    
from __future__ import annotations

__version__ = '0.1.0'

__author__ = 'Corey Rayburn Yung'

__all__: list[str] = [
    'Assembler',
    'Classer',
    'Delegate',
    'Factory',
    'Flexer',
    'Instancer',
    'Manager',
    'Manufacturer',
    'Producer',
    'Registrar',
    'Scribe',
    'Sourcerer',
    'Subclasser',  
    'finalize',
    'inject_attributes',
    'is_constructor',  
    'set_compatibility_rule',
    'set_keyer',
    'set_method_namer',
    'set_overwrite_rule',
    'set_verbose_rule']


from .base import Factory, Manager, Producer
from .configuration import (
    set_compatibility_rule,
    set_keyer,
    set_method_namer,
    set_overwrite_rule,
    set_verbose_rule)
from .dispatchers import Delegate, Sourcerer
from .managers import Assembler
from .producers import Classer, Flexer, Instancer
from .prototypers import Scribe
from .registries import Registrar, Subclasser
from .shared import finalize, inject_attributes, is_constructor
from .storage import Manufacturer
