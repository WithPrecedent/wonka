"""Tests the `wonka` package metadata and namespace."""

from __future__ import annotations

import importlib.metadata
import importlib.resources

import wonka


def test_version() -> None:
    """Tests that the package and installed versions match."""
    assert wonka.__version__ == '0.3.0'
    assert importlib.metadata.version('wonka') == wonka.__version__


def test_all_names_are_exported() -> None:
    """Tests that every name in `__all__` exists in the package."""
    assert 'AutoRegistrar' in wonka.__all__
    assert 'Cluster' in wonka.__all__
    for name in wonka.__all__:
        assert hasattr(wonka, name)


def test_all_is_sorted_and_unique() -> None:
    """Tests that `__all__` has no duplicates and is sorted."""
    assert len(set(wonka.__all__)) == len(wonka.__all__)
    classes = [n for n in wonka.__all__ if n[0].isupper()]
    functions = [n for n in wonka.__all__ if n[0].islower()]
    assert classes == sorted(classes)
    assert functions == sorted(functions)


def test_package_is_typed() -> None:
    """Tests that the package ships the `py.typed` marker."""
    assert importlib.resources.files('wonka').joinpath('py.typed').is_file()


if __name__ == '__main__':
    test_version()
