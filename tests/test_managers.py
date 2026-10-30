"""Tests the `wonka` construction managers."""

from __future__ import annotations

import dataclasses
from typing import Any, ClassVar

import pytest
from conftest import Adder, Doubler

import wonka


@dataclasses.dataclass
class Options(wonka.Subclasser):
    """Base `Subclasser` for the tests."""


@dataclasses.dataclass
class Configuration(Options):
    """Subclass of `Options` with stored contents.

    Args:
        contents: stored settings. Defaults to an empty `dict`.

    """

    contents: dict[str, Any] = dataclasses.field(default_factory = dict)


@dataclasses.dataclass
class RegistrationDesk(wonka.Registrar):
    """`Registrar` with a fixed registry."""

    registry: ClassVar[dict[str, Any]] = {'configuration': Configuration}


def test_assembler_stores_created_constructors() -> None:
    """Tests adding instances created by other factories."""
    assembly_line = wonka.Assembler()
    config = RegistrationDesk.create(
        'configuration',
        parameters = {'contents': {'verbose': True}})
    setup = Options.create(
        'configuration',
        parameters = {'contents': {'ghost': 'town'}})
    assembly_line.add(config)
    assembly_line.add(setup)
    assert list(assembly_line) == [config, setup]


def test_manage_order() -> None:
    """Tests that constructors are called in order."""
    line = wonka.Assembler([Adder, Doubler])
    assert line.manage(1) == 4
    assert line.create(1) == 4
    assert wonka.Assembler([Doubler, Adder]).manage(1) == 3


def test_manage_passes_kwargs() -> None:
    """Tests that keyword arguments are passed to every constructor."""
    line = wonka.Assembler([Adder, Adder])
    assert line.create(0, amount = 5) == 10


def test_manage_empty_returns_item() -> None:
    """Tests that an empty `Assembler` returns the item unchanged."""
    assert wonka.Assembler().manage('x') == 'x'


def test_nested_assembler() -> None:
    """Tests that an `Assembler` can contain another `Assembler`."""
    inner = wonka.Assembler([Adder, Doubler])
    outer = wonka.Assembler([inner, Adder])
    assert outer.manage(1) == 5


def test_add_validates() -> None:
    """Tests that `add` accepts constructors and rejects anything else."""
    line = wonka.Assembler()
    line.add(Adder)
    line.add([Doubler, Adder])
    assert len(line) == 3
    with pytest.raises(TypeError):
        line.add(3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        line.add([Adder, 3])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        line.add('abc')  # type: ignore[arg-type]


def test_add_assembler_as_one_constructor() -> None:
    """Tests that `add` stores an `Assembler` instead of its contents."""
    inner = wonka.Assembler([Adder, Doubler])
    line = wonka.Assembler()
    line.add(inner)
    assert list(line) == [inner]


def test_insert_and_append_validate() -> None:
    """Tests that `insert`, `append`, and `extend` reject non-constructors."""
    line = wonka.Assembler()
    line.append(Adder)
    line.extend([Doubler])
    line.insert(0, Doubler)
    assert list(line) == [Doubler, Adder, Doubler]
    with pytest.raises(TypeError):
        line.append(3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        line.insert(0, 'abc')  # type: ignore[arg-type]
    assert len(line) == 3


def test_sequence_behavior() -> None:
    """Tests indexing, setting, deleting, and searching."""
    line = wonka.Assembler([Adder, Doubler])
    assert line[0] is Adder
    line[0] = Doubler
    assert list(line) == [Doubler, Doubler]
    del line[0]
    assert list(line) == [Doubler]
    line.insert(0, Adder)
    assert line.index(Adder) == 0
    assert Doubler in line
    assert list(reversed(line)) == [Doubler, Adder]
    assert line.count(Adder) == 1


def test_slices() -> None:
    """Tests getting, setting, and deleting slices."""
    line = wonka.Assembler([Adder, Doubler, Adder])
    assert line[1:] == [Doubler, Adder]
    line[0:2] = [Doubler]
    assert list(line) == [Doubler, Adder]
    del line[:1]
    assert list(line) == [Adder]
    with pytest.raises(TypeError):
        line[0:1] = [3]  # type: ignore[list-item]
    assert list(line) == [Adder]


def test_setitem_validates() -> None:
    """Tests that setting an index rejects non-constructors."""
    line = wonka.Assembler([Adder])
    with pytest.raises(TypeError):
        line[0] = 3  # type: ignore[call-overload]
    assert list(line) == [Adder]


def test_delete() -> None:
    """Tests `delete` with an index, a slice, and a missing index."""
    line = wonka.Assembler([Adder, Doubler, Adder])
    line.delete(0)
    assert list(line) == [Doubler, Adder]
    line.delete(slice(0, 1))
    assert list(line) == [Adder]
    with pytest.raises(IndexError):
        line.delete(5)


def test_prepend() -> None:
    """Tests prepending one constructor or a sequence of constructors."""
    line = wonka.Assembler([Doubler])
    line.prepend(Adder)
    assert list(line) == [Adder, Doubler]
    line.prepend([Doubler, Doubler])
    assert list(line) == [Doubler, Doubler, Adder, Doubler]


def test_prepend_assembler_as_one_constructor() -> None:
    """Tests that `prepend` stores an `Assembler` instead of its contents."""
    inner = wonka.Assembler([Adder, Doubler])
    line = wonka.Assembler([Doubler])
    line.prepend(inner)
    assert list(line) == [inner, Doubler]


def test_prepend_validates() -> None:
    """Tests that `prepend` rejects non-constructors."""
    line = wonka.Assembler([Doubler])
    with pytest.raises(TypeError):
        line.prepend(3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        line.prepend('abc')  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        line.prepend([Adder, 3])  # type: ignore[list-item]
    assert list(line) == [Doubler]


def test_subset() -> None:
    """Tests `subset` with `include`, `exclude`, or both."""
    line = wonka.Assembler([Adder, Doubler])
    assert list(line.subset(include = Adder)) == [Adder]
    assert list(line.subset(exclude = Adder)) == [Doubler]
    subset = line.subset(include = [Adder, Doubler], exclude = Doubler)
    assert list(subset) == [Adder]
    assert list(line) == [Adder, Doubler]
    with pytest.raises(ValueError, match = 'include or exclude'):
        line.subset()


def test_subset_returns_new_instance() -> None:
    """Tests that `subset` does not share `contents` with the original."""
    line = wonka.Assembler([Adder])
    subset = line.subset(include = Adder)
    assert isinstance(subset, wonka.Assembler)
    subset.add(Doubler)
    assert list(line) == [Adder]


def test_add_operator_returns_copy() -> None:
    """Tests that `+` returns a new instance and leaves both unchanged."""
    line = wonka.Assembler([Adder])
    combined = line + Doubler
    assert combined is not line
    assert list(combined) == [Adder, Doubler]
    assert list(line) == [Adder]
    assert list(line + [Doubler, Doubler]) == [Adder, Doubler, Doubler]
    with pytest.raises(TypeError):
        line + 3  # type: ignore[operator]


def test_inplace_add_operator() -> None:
    """Tests that `+=` adds to the instance in place."""
    line = wonka.Assembler()
    original = line
    line += Adder
    line += [Doubler]
    assert line is original
    assert list(line) == [Adder, Doubler]


if __name__ == '__main__':
    test_assembler_stores_created_constructors()
