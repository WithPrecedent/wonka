"""wonka settings and convenience functions for changing those settings.

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

import camina


_KEY_NAMER: Callable[[object | type[Any]], str] = camina.namify
_METHOD_NAMER: Callable[[object | type[Any]], str] = (lambda x: f'from_{x}')
_OVERWRITE: bool = True
_STRICT_COMPATIBILITY: bool = True
_VERBOSE: bool = False


def set_compatibility_rule(compatibility: bool) -> None:
    """Sets the global attribute compatibility rule.

    Args:
        compatibility (bool): whether to require the 'is_constructor' method to
            use strict or relaxed validation.


    Raises:
        TypeError: if 'compatibility' is not bool.

    """
    if isinstance(compatibility, bool):
        globals()["_STRICT_COMPATIBILITY"] = compatibility
    else:
        raise TypeError('compatibility argument must be boolean')

def set_keyer(keyer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name dict keys.

    Args:
        keyer (Callable[[object | type[Any]], str]): function that returns a
            str name of any item passed.

    Raises:
        TypeError: if 'keyer' is not callable.

    """
    if isinstance(keyer, Callable):
        globals()["_KEY_NAMER"] = keyer
    else:
        raise TypeError('keyer argument must be a callable')

def set_method_namer(namer: Callable[[object | type[Any]], str]) -> None:
    """Sets the global default function used to name factory creation methods.

    Args:
        namer (Callable[[object | type[Any]], str]): function that returns a
            str name of any item passed.

    Raises:
        TypeError: if 'keyer' is not callable.

    """
    if isinstance(namer, Callable):
        globals()["_METHOD_NAMER"] = namer
    else:
        raise TypeError('namerargument must be a callable')

def set_overwrite_rule(overwrite: bool) -> None:
    """Sets the global attribute overwrite rule.

    Args:
        overwrite (bool): whether to set the default rule to overwrite existing
            attributes.

    Raises:
        TypeError: if 'overwrite' is not bool.

    """
    if isinstance(overwrite, bool):
        globals()["_OVERWRITE"] = overwrite
    else:
        raise TypeError('overwrite argument must be boolean')

def set_verbose_rule(verbose: bool) -> None:
    """Sets the global attribute message verbosity rule.

    Args:
        verbose (bool): whether to set the default rule to verbosity in logging
            and messaging.

    Raises:
        TypeError: if 'verbose' is not bool.

    """
    if isinstance(verbose, bool):
        globals()["_VERBOSE"] = verbose
    else:
        raise TypeError('verbose argument must be boolean')


# @dataclasses.dataclass
# class _MISSING_VALUE(object):
#     """Sentinel object for a missing data or parameter.

#     This follows the same pattern as the '__MISSING_TYPE' class in the builtin
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

