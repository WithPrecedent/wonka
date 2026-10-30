"""Flexible, accessible, extensible Python factories

Contents:
    Assembler: assembly line constructor that calls stored constructors in
        order.
    AutoRegistrar: `Registrar` that automatically registers its subclasses.
    Classer: producer that always returns a class.
    Cluster: base class for collections of constructors.
    Delegate: dispatcher that calls a creation method named after the type of
        the item passed.
    Factory: base class for `wonka` constructors.
    Flexer: producer that returns an instance only when parameters are passed.
    Instancer: producer that always returns an instance.
    Manager: base class for iterable constructors.
    Manufacturer: `dict`-like container of constructors.
    Producer: base mixin for modifying created items.
    Registrar: factory that builds items from a registry.
    Scribe: factory that clones items.
    Sourcerer: dispatcher that calls a creation method based on the types in
        its `sources`.
    Subclasser: factory that builds items from the subclasses of a class.
    finalize: finalizes construction before returning a value.
    inject_attributes: adds keys and values of a mapping to an item as
        attributes.
    is_constructor: returns whether an item is a `wonka`-compatible
        constructor.
    set_compatibility_rule: sets the global attribute compatibility rule.
    set_keyer: sets the global default function used to name dict keys.
    set_method_namer: sets the global default function used to name factory
        creation methods.
    set_overwrite_rule: sets the global attribute overwrite rule.
    set_verbose_rule: sets the global attribute message verbosity rule.

"""

from __future__ import annotations

__version__ = '0.3.0'

__author__: str = 'Corey Rayburn Yung'

__all__: list[str] = [
    'Assembler',
    'AutoRegistrar',
    'Classer',
    'Cluster',
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


from .base import Cluster, Factory, Manager, Producer
from .clusters import Manufacturer
from .dispatchers import Delegate, Sourcerer
from .managers import Assembler
from .options import (
    set_compatibility_rule,
    set_keyer,
    set_method_namer,
    set_overwrite_rule,
    set_verbose_rule,
)
from .producers import Classer, Flexer, Instancer
from .prototypers import Scribe
from .registries import AutoRegistrar, Registrar, Subclasser
from .shared import finalize, inject_attributes, is_constructor
