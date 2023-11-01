"""Configuration settings and convenience functions for changing those settings.

Contents:
    set_compatibility_rule: sets the global attribute compatibility rule.
    set_keyer: sets the global default function used to name dict keys.
    set_method_namer: sets the global default function used to name factory
        creation methods.
    set_overwrite_rule: sets the global attribute overwrite rule.
    set_verbose_rule: sets the global attribute message verbosity rule.

"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from . import utilities

# Default naming function for non-str objects.
_KEY_NAMER: Callable[[object | type[Any]], str] = utilities._namify
# Default naming convention for dispatcher registry creation methods.
_METHOD_NAMER: Callable[[object | type[Any]], str] = lambda x: f'from_{x}'
# Whether to overwrite existing attributes when arguments are passed to create
# an item that is already an instance or has class attributes of the same name
# as in the passed arguments.
_OVERWRITE: bool = True
# Whether to validate an object as a subclass of a `wonka`-constructor or to
# support duck typing by not validating an object before its use.
_STRICT_COMPATIBILITY: bool = True
# Whether to return more elaborate error messages and feedback.
_VERBOSE: bool = False


def set_compatibility_rule(compatibility: bool) -> None:
    """Sets the global attribute compatibility rule.

    Args:
        compatibility: whether to require the `is_constructor` method to use
            strict or relaxed validation.

    Raises:
        TypeError: if `compatibility` is not `bool`.

    """
    if isinstance(compatibility, bool):
        globals()["_STRICT_COMPATIBILITY"] = compatibility
    else:
        raise TypeError('compatibility argument must be boolean')

def set_keyer(keyer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name `dict` keys.

    Args:
        keyer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if `keyer` is not callable.

    """
    if isinstance(keyer, Callable):
        globals()["_KEY_NAMER"] = keyer
    else:
        raise TypeError('keyer argument must be a callable')

def set_method_namer(namer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name factory creation methods.

    Args:
        namer: function that returns a `str` name of any item passed.

    Raises:
        TypeError: if 'keyer' is not callable.

    """
    if isinstance(namer, Callable):
        globals()["_METHOD_NAMER"] = namer
    else:
        raise TypeError('namer argument must be a callable')

def set_overwrite_rule(overwrite: bool) -> None:
    """Sets the global attribute overwrite rule.

    Args:
        overwrite: whether to set the default rule to overwrite existing
            attributes.

    Raises:
        TypeError: if `overwrite` is not bool.

    """
    if isinstance(overwrite, bool):
        globals()["_OVERWRITE"] = overwrite
    else:
        raise TypeError('overwrite argument must be boolean')

def set_verbose_rule(verbose: bool) -> None:
    """Sets the global attribute message verbosity rule.

    Args:
        verbose: whether to set the default rule to verbosity in logging and
            messaging.

    Raises:
        TypeError: if `verbose` is not bool.

    """
    if isinstance(verbose, bool):
        globals()["_VERBOSE"] = verbose
    else:
        raise TypeError('verbose argument must be boolean')


# @dataclasses.dataclass
# class _MISSING_VALUE(object):
#     """Sentinel object for a missing data or parameter.

#     This follows the same pattern as the '__MISSING_TYPE` class in the builtin
#     dataclasses library.
#     https://github.com/python/cpython/blob/3.10/Lib/dataclasses.py#L182-L186

#     Because None is sometimes a valid argument or data option, this class
#     provides an alternative that does not create the confusion that a default of
#     None can sometimes lead to.

#     """
#     pass


# # _MISSING, instance of _MISSING_VALUE, should be used for missing values as an
# # alternative to None when None is a valid value for an argument. This provides
# # a fuller repr and traceback.
# _MISSING = _MISSING_VALUE()
