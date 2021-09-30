#from collections.abc import MutableMapping
from typing import AbstractSet, Dict, Iterator, TypeVar, Mapping, Set, MutableMapping, Generic
import typing

KT = TypeVar('KT')
VT = TypeVar('VT')


class JournaledMapping(MutableMapping[KT, VT], Generic[KT, VT]):
    def __init__(self, lower: Mapping[KT, VT]):
        self.lower = lower
        self.top: Dict[KT, VT] = dict()
        self.deleted: Set[KT] = set()

    def keys(self) -> AbstractSet[KT]:
        return (self.lower.keys() | self.top.keys()) - self.deleted

    def __getitem__(self, k) -> VT:
        if k in self.deleted:
            raise KeyError(k)
        if k in self.top:
            return self.top[k]
        return self.lower[k]

    def __setitem__(self, k: KT, v: VT):
        self.deleted.discard(k)
        self.top[k] = v

    def __delitem__(self, k: KT) -> None:
        if k in self.deleted:
            raise KeyError(k)
        found = False
        if k in self.lower:
            self.deleted.add(k)
            found = True
        if k in self.top:
            del self.top[k]
            found = True
        if not found:
            raise KeyError(k)

    def __iter__(self) -> Iterator[KT]:
        return self.keys().__iter__()

    def __len__(self) -> int:
        return len(self.keys())

# TESTS

_base_dict = {"lower": True, "deleted" : False, "overwrite" : False}
_base_dict_copy = _base_dict.copy()

def jm():
    jm = JournaledMapping(_base_dict)
    del jm["deleted"]
    jm["overwrite"] = True
    jm["top"] = True
    return jm


def test_basic(jm):
    assert jm["lower"]
    assert jm["top"]
    assert jm["overwrite"]
    assert "deleted" not in jm

def _test_delete(jm, key):
    del jm[key]
    assert key not in jm, "failed to delete" 
    try:
        del jm[key]
    except KeyError:
        pass
    else:
        raise Exception("double delete should fail")

def test_iter(jm: JournaledMapping):
    for k,v in jm.items():
        print(k,v)

def test_keys(jm: JournaledMapping):
    keys = jm.keys()
    assert keys == {'lower', 'top', 'overwrite'}

def test_delete_top(jm):
    return _test_delete(jm, "top")

def test_delete_lower(jm):
    return _test_delete(jm, "lower")

test_delete_top(jm())
test_delete_lower(jm())
test_iter(jm())
test_keys(jm())

for x in _base_dict.__iter__():
    print(x)