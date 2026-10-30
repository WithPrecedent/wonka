"""Shared fixtures and example constructors for the `wonka` tests.

Contents:
    Adder: factory that adds an amount to an integer.
    Doubler: factory that doubles an integer.
    Thing: simple dataclass used as a created item.
    restore_options: fixture that restores the global `wonka` options after
        each test.

"""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any

import pytest

import wonka
from wonka import options

if TYPE_CHECKING:
    from collections.abc import Iterator

_OPTION_NAMES: tuple[str, ...] = (
    '_KEY_NAMER',
    '_METHOD_NAMER',
    '_OVERWRITE',
    '_STRICT_COMPATIBILITY',
    '_VERBOSE')


@dataclasses.dataclass
class Thing:
    """Simple dataclass used as a created item.

    Args:
        value: stored value. Defaults to 0.

    """

    value: int = 0


@dataclasses.dataclass
class Adder(wonka.Factory):
    """Factory that adds `amount` to an integer."""

    @classmethod
    def create(cls, item: int, amount: int = 1, **kwargs: Any) -> int:
        """Returns `item` plus `amount`.

        Args:
            item: integer to add to.
            amount: amount to add. Defaults to 1.
            **kwargs: ignored keyword arguments.

        Returns:
            The sum of `item` and `amount`.

        """
        return item + amount


@dataclasses.dataclass
class Doubler(wonka.Factory):
    """Factory that doubles an integer."""

    @classmethod
    def create(cls, item: int, **kwargs: Any) -> int:
        """Returns `item` doubled.

        Args:
            item: integer to double.
            **kwargs: ignored keyword arguments.

        Returns:
            Twice `item`.

        """
        return item * 2


@pytest.fixture(autouse = True)
def restore_options() -> Iterator[None]:
    """Restores the global `wonka` options after each test.

    `pytest-randomly` shuffles the order of the tests, so a test that changes a
    global option must not affect the tests that run after it.

    Yields:
        None: control passes to the test, and then the options are restored.

    """
    saved = {name: getattr(options, name) for name in _OPTION_NAMES}
    yield
    for name, value in saved.items():
        setattr(options, name, value)
