"""Edge case and regression tests for wonka."""

from __future__ import annotations

import dataclasses
import pathlib
from collections.abc import MutableMapping
from typing import Any, ClassVar

import pytest

import wonka
from wonka import base, dispatchers, options, shared, utilities


@dataclasses.dataclass
class Thing:
    value: int = 0


@dataclasses.dataclass
class Maker(wonka.Sourcerer):
    value: Any = None
    sources: ClassVar[dict[Any, str]] = {
        int: "number",
        MutableMapping: "mapping",
        str: "text",
    }

    @classmethod
    def from_number(cls, item: int) -> Maker:
        return cls(value = item)

    @classmethod
    def from_mapping(cls, item: dict) -> Maker:
        return cls(value = dict(item))

    @classmethod
    def from_text(cls, item: str) -> Maker:
        return cls(value = item)


@dataclasses.dataclass
class Broken(wonka.Sourcerer):
    sources: ClassVar[dict[Any, str]] = {int: "missing", str: "boom"}

    @classmethod
    def from_boom(cls, item: str) -> Any:
        raise AttributeError("internal failure")


# Dispatchers


def test_sourcerer_skips_non_matching_kinds():
    assert Maker.create("hi").value == "hi"
    assert Maker.create({"a": 1}).value == {"a": 1}
    assert Maker.create(3).value == 3


def test_sourcerer_no_match():
    with pytest.raises(KeyError):
        Maker.create(3.5)


def test_is_kind():
    assert dispatchers._is_kind(bool, int)
    assert dispatchers._is_kind(True, int)
    assert not dispatchers._is_kind("x", int)
    assert not dispatchers._is_kind(str, int)


def test_missing_builder_method():
    with pytest.raises(AttributeError, match = "from_missing"):
        Broken.create(1)


def test_builder_attribute_error_not_masked():
    with pytest.raises(AttributeError, match = "internal failure"):
        Broken.create("x")


def test_delegate_no_method():
    class Empty(wonka.Delegate):
        pass

    with pytest.raises(AttributeError):
        Empty.create(1)


# Scribe


@dataclasses.dataclass
class Clone(wonka.Scribe):
    contents: list = dataclasses.field(default_factory = list)


def test_scribe_clones_falsy_items():
    assert wonka.Scribe.create(0) == 0
    assert wonka.Scribe.create("") == ""
    assert wonka.Scribe.create([]) == []


def test_scribe_deep_copies():
    original = [[1], [2]]
    copied = wonka.Scribe.create(original)
    assert copied == original
    assert copied is not original
    assert copied[0] is not original[0]


def test_scribe_none_clones_self():
    assert Clone.create() is Clone  # deepcopy of a class is the class


# shared


def test_finalize_class_with_parameters():
    assert shared.finalize(Thing, {"value": 4}).value == 4


def test_finalize_instance_with_parameters():
    thing = Thing()
    result = shared.finalize(thing, {"value": 9})
    assert result is thing
    assert thing.value == 9


def test_finalize_without_parameters():
    assert shared.finalize(Thing) is Thing


def test_inject_attributes_overwrite_rules():
    thing = Thing(value = 1)
    shared.inject_attributes(thing, {"value": 2}, overwrite = False)
    assert thing.value == 1
    shared.inject_attributes(thing, {"value": 2}, overwrite = True)
    assert thing.value == 2
    assert shared.inject_attributes(thing, None) is thing


def test_is_constructor_strict_and_relaxed():
    class Duck:
        @classmethod
        def create(cls, item: Any) -> Any:
            return item

    try:
        wonka.set_compatibility_rule(True)
        assert shared.is_constructor(wonka.Scribe)
        assert shared.is_constructor(wonka.Assembler())
        assert not shared.is_constructor(Duck)
        assert not shared.is_constructor(3)
        wonka.set_compatibility_rule(False)
        assert shared.is_constructor(Duck)
        assert not shared.is_constructor(3)
    finally:
        wonka.set_compatibility_rule(True)


# options


@pytest.mark.parametrize(
    ("setter", "bad"),
    [
        (wonka.set_compatibility_rule, "yes"),
        (wonka.set_overwrite_rule, 1),
        (wonka.set_verbose_rule, None),
        (wonka.set_keyer, "not callable"),
        (wonka.set_method_namer, 5),
    ],
)
def test_option_setters_validate(setter, bad):
    with pytest.raises(TypeError):
        setter(bad)


def test_option_setters_set_values():
    originals = (options._OVERWRITE, options._VERBOSE, options._METHOD_NAMER)
    try:
        wonka.set_overwrite_rule(False)
        wonka.set_verbose_rule(True)
        wonka.set_method_namer(lambda x: f"make_{x}")
        assert options._OVERWRITE is False
        assert options._VERBOSE is True
        assert options._METHOD_NAMER("a") == "make_a"
    finally:
        options._OVERWRITE, options._VERBOSE, options._METHOD_NAMER = originals


# utilities


def test_snakify():
    assert utilities._snakify("HTTPServer") == "http_server"
    assert utilities._snakify("FastPlugin") == "fast_plugin"
    assert utilities._snakify("already_snake") == "already_snake"


def test_namify():
    assert utilities._namify("abc") == "abc"
    assert utilities._namify(Thing) == "thing"
    assert utilities._namify(Thing()) == "thing"

    class Named:
        name = "given"

    assert utilities._namify(Named()) == "given"


def test_iterify():
    assert list(utilities._iterify(None)) == []
    assert list(utilities._iterify("abc")) == ["abc"]
    assert list(utilities._iterify(5)) == [5]
    assert list(utilities._iterify([1, 2])) == [1, 2]


def test_is_sequence():
    assert utilities._is_sequence([1])
    assert utilities._is_sequence((1,))
    assert not utilities._is_sequence("abc")
    assert utilities._is_sequence("abc", include_str = True)
    assert not utilities._is_sequence({1})


def test_pathlibify():
    assert utilities._pathlibify("a/b") == pathlib.Path("a/b")
    path = pathlib.Path("x")
    assert utilities._pathlibify(path) is path
    with pytest.raises(TypeError):
        utilities._pathlibify(3)


# Subclasser / Registrar


@dataclasses.dataclass
class Root(wonka.Subclasser):
    pass


@dataclasses.dataclass
class Branch(Root):
    pass


@dataclasses.dataclass
class Leaf(Branch):
    pass


def test_subclasser_indirect_and_missing():
    assert Root.create("leaf") is Leaf
    assert isinstance(Root.create("branch", {}), Branch)
    with pytest.raises(KeyError):
        Root.create("root")


def test_registrar_missing_key():
    class Desk(wonka.Registrar):
        registry: ClassVar[dict] = {"thing": Thing}

    assert Desk.create("thing", {"value": 2}).value == 2
    with pytest.raises(KeyError, match = "nope"):
        Desk.create("nope")


# Assembler


@dataclasses.dataclass
class Adder(wonka.Factory):
    @classmethod
    def create(cls, item: int, amount: int = 1, **kwargs: Any) -> int:
        return item + amount


@dataclasses.dataclass
class Doubler(wonka.Factory):
    @classmethod
    def create(cls, item: int, **kwargs: Any) -> int:
        return item * 2


def test_assembler_manage_order():
    line = wonka.Assembler([Adder, Doubler])
    assert line.manage(1) == 4
    assert line.create(1) == 4
    assert wonka.Assembler([Doubler, Adder]).manage(1) == 3


def test_assembler_passes_kwargs():
    line = wonka.Assembler([Adder, Adder])
    assert line.create(0, amount = 5) == 10


def test_assembler_empty_returns_item():
    assert wonka.Assembler().manage("x") == "x"


def test_assembler_add_validates():
    line = wonka.Assembler()
    line.add(Adder)
    line.add([Doubler, Adder])
    assert len(line) == 3
    with pytest.raises(TypeError):
        line.add(3)
    with pytest.raises(TypeError):
        line.add([Adder, 3])
    with pytest.raises(TypeError):
        line.add("abc")


def test_assembler_sequence_behavior():
    line = wonka.Assembler([Adder, Doubler])
    assert line[0] is Adder
    line[0] = Doubler
    assert list(line) == [Doubler, Doubler]
    del line[0]
    assert list(line) == [Doubler]
    line.insert(0, Adder)
    assert line.index(Adder) == 0
    assert Doubler in line


def test_assembler_prepend():
    line = wonka.Assembler([Doubler])
    line.prepend(Adder)
    assert list(line) == [Adder, Doubler]
    line.prepend([Doubler, Doubler])
    assert list(line) == [Doubler, Doubler, Adder, Doubler]


def test_assembler_subset():
    line = wonka.Assembler([Adder, Doubler])
    assert list(line.subset(include = Adder)) == [Adder]
    assert list(line.subset(exclude = Adder)) == [Doubler]
    assert list(line.subset(include = [Adder, Doubler], exclude = Doubler)) == [
        Adder
    ]
    assert list(line) == [Adder, Doubler]
    with pytest.raises(ValueError, match = "include or exclude"):
        line.subset()


def test_assembler_add_operator():
    line = wonka.Assembler()
    line + Adder
    assert list(line) == [Adder]


# Manufacturer / Cluster


def test_manufacturer_add_validation():
    depot = wonka.Manufacturer()
    with pytest.raises(TypeError):
        depot.add(3)
    with pytest.raises(TypeError):
        depot.add({"ok": Adder, "bad": 3})
    assert len(depot) == 0


def test_manufacturer_mapping_interface():
    depot = wonka.Manufacturer()
    depot.add(Adder)
    depot.add({"doubler": Doubler})
    assert depot.keys() == ("adder", "doubler")
    assert depot.values() == (Adder, Doubler)
    assert depot.items() == (("adder", Adder), ("doubler", Doubler))
    assert depot["adder"] is Adder
    assert list(depot) == ["adder", "doubler"]
    del depot["adder"]
    assert len(depot) == 1
    with pytest.raises(KeyError):
        del depot["adder"]


def test_cluster_is_abstract():
    assert issubclass(wonka.Manufacturer, wonka.Cluster)
    with pytest.raises(TypeError):
        wonka.Cluster()


def test_manufacturer_setitem_and_add_operator():
    depot = wonka.Manufacturer()
    depot["x"] = Adder
    depot + Doubler
    assert depot["x"] is Adder
    assert depot["doubler"] is Doubler


# Producers


def test_producers_directly():
    thing = Thing()
    assert wonka.Classer.produce(thing) is Thing
    assert wonka.Classer.produce(Thing) is Thing
    assert wonka.Instancer.produce(Thing) == Thing()
    assert wonka.Instancer.produce(Thing, {"value": 3}).value == 3
    assert wonka.Instancer.produce(thing) is thing
    assert wonka.Flexer.produce(Thing) is Thing
    assert wonka.Flexer.produce(Thing, {"value": 5}).value == 5
    assert wonka.Flexer.produce(thing, {"value": 6}) is thing
    assert thing.value == 6


def test_base_abstract_interfaces():
    with pytest.raises(TypeError):
        base.Factory()
    with pytest.raises(TypeError):
        base.Manager([])
    with pytest.raises(TypeError):
        base.Producer()
