"""Tests the global `wonka` options and their setters."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

import wonka
from wonka import options


@pytest.mark.parametrize(
    ('setter', 'bad'),
    [
        (wonka.set_compatibility_rule, 'yes'),
        (wonka.set_overwrite_rule, 1),
        (wonka.set_verbose_rule, None),
        (wonka.set_keyer, 'not callable'),
        (wonka.set_method_namer, 5)])
def test_setters_validate(setter: Callable[[Any], None], bad: Any) -> None:
    """Tests that each setter rejects a value of the wrong type.

    Args:
        setter: option setter to test.
        bad: invalid value for the setter.

    """
    with pytest.raises(TypeError):
        setter(bad)


def test_setters_set_values() -> None:
    """Tests that each setter changes its global option."""
    wonka.set_compatibility_rule(False)
    wonka.set_overwrite_rule(False)
    wonka.set_verbose_rule(True)
    wonka.set_method_namer(lambda x: f'make_{x}')
    wonka.set_keyer(str)
    assert options._STRICT_COMPATIBILITY is False
    assert options._OVERWRITE is False
    assert options._VERBOSE is True
    assert options._METHOD_NAMER('a') == 'make_a'
    assert options._KEY_NAMER is str


def test_defaults() -> None:
    """Tests the default values of the global options."""
    assert options._STRICT_COMPATIBILITY is True
    assert options._OVERWRITE is True
    assert options._VERBOSE is False
    assert options._METHOD_NAMER('dict') == 'from_dict'
    assert options._KEY_NAMER(wonka.Scribe) == 'scribe'
