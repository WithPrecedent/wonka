"""Configuration settings and convenience functions for changing those settings.

Contents:
    set_compatibility_rule: sets the global attribute compatibility rule.
    set_keyer: sets the global default function used to name dict keys.
    set_method_namer: sets the global default function used to name factory
        creation methods.
    set_overwrite_rule: sets the global attribute overwrite rule.
    set_verbose_rule: sets the global attribute message verbosity rule.
    _KEY_NAMER: default function that names non-`str` objects.
    _METHOD_NAMER: default naming convention for dispatcher creation methods.
    _OVERWRITE: whether to overwrite existing attributes when parameters are
        injected into an item.
    _STRICT_COMPATIBILITY: whether `is_constructor` requires a `wonka` class or
        accepts any object with a `create` method.
    _VERBOSE: whether to return more elaborate error messages and feedback.

"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from . import utilities

# Default naming function for non-str objects.
_KEY_NAMER: Callable[[Any], str] = utilities._namify
# Default naming convention for dispatcher registry creation methods.
_METHOD_NAMER: Callable[[Any], str] = lambda x: f'from_{x}'
# Whether to overwrite existing attributes when arguments are passed to create
# an item that is already an instance or has class attributes of the same name
# as in the passed arguments.
_OVERWRITE: bool = True
# Whether to validate an object as a subclass of a `wonka`-constructor or to
# support duck typing by not validating an object before its use.
_STRICT_COMPATIBILITY: bool = True
# Whether to return more elaborate error messages and feedback.
_VERBOSE: bool = False

""" Public Functions """


def set_compatibility_rule(compatibility: bool) -> None:
    """Sets the global attribute compatibility rule.

    Args:
        compatibility: whether to require the `is_constructor` method to use
            strict or relaxed validation.

    Raises:
        TypeError: if `compatibility` is not `bool`.

    """
    if not isinstance(compatibility, bool):
        message = 'compatibility argument must be boolean'
        raise TypeError(message)
    globals()['_STRICT_COMPATIBILITY'] = compatibility


def set_keyer(keyer: Callable[[Any], str]) -> None:
    """Sets the global default function used to name `dict` keys.

    Args:
        keyer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if `keyer` is not callable.

    """
    if not callable(keyer):
        message = 'keyer argument must be a callable'
        raise TypeError(message)
    globals()['_KEY_NAMER'] = keyer


def set_method_namer(namer: Callable[[Any], str]) -> None:
    """Sets the global default function used to name factory creation methods.

    Args:
        namer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if `namer` is not callable.

    """
    if not callable(namer):
        message = 'namer argument must be a callable'
        raise TypeError(message)
    globals()['_METHOD_NAMER'] = namer


def set_overwrite_rule(overwrite: bool) -> None:
    """Sets the global attribute overwrite rule.

    Args:
        overwrite: whether to set the default rule to overwrite existing
            attributes.

    Raises:
        TypeError: if `overwrite` is not `bool`.

    """
    if not isinstance(overwrite, bool):
        message = 'overwrite argument must be boolean'
        raise TypeError(message)
    globals()['_OVERWRITE'] = overwrite


def set_verbose_rule(verbose: bool) -> None:
    """Sets the global attribute message verbosity rule.

    Args:
        verbose: whether to set the default rule to verbosity in logging and
            messaging.

    Raises:
        TypeError: if `verbose` is not `bool`.

    """
    if not isinstance(verbose, bool):
        message = 'verbose argument must be boolean'
        raise TypeError(message)
    globals()['_VERBOSE'] = verbose
