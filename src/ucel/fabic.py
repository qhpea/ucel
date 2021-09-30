import collections
import dataclasses
from abc import abstractmethod
from typing import List, Type
from .getable import Getable

import os
import json


class DatastoreBacked:
    owned: bool
    id: str
    sync: bool
    pass


class Fabric:
    "A (filesystem backed) comunication layer"

    def __init__(self, *, base="/mnt/ucel", slice=[]) -> None:
        self.base = base
        self.slice = slice

    @property
    def id(self):
        return "fabric"

    def path(self, key):
        "get path to stored data"
        return os.path.join(*self.base, *self.slice, *key, ".json")

    def get(self, key):
        path = self.path(key)
        if not os.path.exists(path):
            return None
        if os.path.isfile(path):
            with open(path, "r") as file:
                return json.load(file.read)
        raise Exception(f"{path} is a directory")

    def set(self, key, value):
        pass

    def sub(self, key):
        return Fabric(base=self.base, slice=self.slice + key)




def fabric_backed(cls: Type):
    """
    Convert a dataclass to be backed by fabric.
    Generates properties for all of the fields.
    """
    fields = list(dataclasses.fields(cls))
    print(fields)
    
    def __init__(self, parent: "NestedFabric", id: str) -> None:
        self.fabric = parent.fabric.sub([self.path_in_parent(), id])
        self._dirty = set_cached()
 
        cls.super().__init__(parent, id)
        self.load()

    for field in fields:
        name = field.name
        back_name = "_"+field.name

        setattr(cls, back_name, getattr(cls, name))
        
        # should this be represented as a sub directory insted of a leaf
        is_child = False

        def get_cached(self):
            return getattr(self, back_name)
        
        def set_cached(self, value):
            self._dirty.add(name)
            setattr(self, back_name, value)

        def get_fabric(self):
            value = self.fabric.get(name)
            setattr(self, back_name, value)
            self._dirty.discard(name)
            return value
        
        def set_fabric(self, value):
            setattr(self, back_name, value)
            self._dirty.discard(name)


        setattr(cls, "get_"+name, get_cached)
        setattr(cls, "set_"+name, set_cached)

        prop = property(get_cached, set_cached)

    def sync(self):
        "Set all set values, load all others."

    def load(self, props: List[str] = None):
        """get props from fabric. if None, load all"""
        print(fields)
        pass
    
    cls.sync = sync
    cls.__init__ = __init__
    cls.load = load


class NestedFabric(Getable):
    fabric: Fabric
    pulse: str = None

    @classmethod
    def get_instance(cls, parent, id):
        fabric = parent.fabric
        return cls(fabric, id)

    def sync(self, props: List[str] = None):
        """Syncs all props with fabric. if None, syncs all (default)"""
        pass


