""" Tests wonka prototyper factories. """
from __future__ import annotations
import dataclasses

import wonka


@dataclasses.dataclass
class Clone(wonka.Scribe):

    contents: dict[str, wonka.Factory] = dataclasses.field(
        default_factory = lambda: {'tree': 'house', 'ghost': 'town'})


def test_scribe():
    clone_class = Clone.create()
    clone_instance = clone_class()
    assert clone_instance.contents['tree'] == 'house'
    assert isinstance(clone_instance, Clone)
    new_clone_instance = Clone.create(parameters = {})
    assert new_clone_instance.contents['ghost'] == 'town'
    assert isinstance(new_clone_instance, Clone)
    return

if __name__ == '__main__':
    test_scribe()
