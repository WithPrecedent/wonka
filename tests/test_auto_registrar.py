"""Tests wonka `AutoRegistrar`."""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest

import wonka


@dataclasses.dataclass
class Plugin(wonka.AutoRegistrar):
    contents: dict[str, Any] = dataclasses.field(default_factory = dict)


@dataclasses.dataclass
class FastPlugin(Plugin):
    pass


@dataclasses.dataclass
class SlowPlugin(FastPlugin):
    pass


@dataclasses.dataclass
class Gadget(wonka.AutoRegistrar):
    pass


@dataclasses.dataclass
class Widget(Gadget):
    pass


def test_exported():
    assert "AutoRegistrar" in wonka.__all__
    assert "Cluster" in wonka.__all__
    for name in wonka.__all__:
        assert hasattr(wonka, name)


def test_subclasses_registered_including_indirect():
    assert Plugin.registry["fast_plugin"] is FastPlugin
    assert Plugin.registry["slow_plugin"] is SlowPlugin
    assert Plugin.registry["plugin"] is Plugin


def test_families_do_not_share_registries():
    assert Plugin.registry is not Gadget.registry
    assert wonka.AutoRegistrar.registry == {}
    assert "widget" in Gadget.registry
    assert "widget" not in Plugin.registry
    assert "fast_plugin" not in Gadget.registry


def test_create_from_registry():
    plugin = Plugin.create("fast_plugin", parameters = {"contents": {"a": 1}})
    assert isinstance(plugin, FastPlugin)
    assert plugin.contents == {"a": 1}


def test_create_without_parameters_returns_class():
    assert Plugin.create("slow_plugin") is SlowPlugin


def test_create_missing_key():
    with pytest.raises(KeyError):
        Plugin.create("nope")


def test_custom_keyer():
    original = wonka.options._KEY_NAMER
    try:
        wonka.set_keyer(lambda x: f"k_{x.__name__}")

        @dataclasses.dataclass
        class Custom(Plugin):
            pass

        assert Plugin.registry["k_Custom"] is Custom
    finally:
        wonka.set_keyer(original)
