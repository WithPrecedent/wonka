"""Flexible, accessible, extensible Python factories"""

from __future__ import annotations

__version__ = '0.1.2'

__author__: str = 'Corey Rayburn Yung'

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
    set_verbose_rule,
)
from .dispatchers import Delegate, Sourcerer
from .managers import Assembler
from .producers import Classer, Flexer, Instancer
from .prototypers import Scribe
from .registries import Registrar, Subclasser
from .shared import finalize, inject_attributes, is_constructor
from .storage import Manufacturer
