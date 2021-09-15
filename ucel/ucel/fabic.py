from abc import abstractmethod
from typing import List
from ucel.gettable import Nested

import os
import json


class DatastoreBacked:
    owned: bool
    id: str
    sync: bool
    pass


class Fabric:
    "A comunication layer"

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


class NestedFabric(Nested):
    fabric: Fabric
    pulse: str = None

    def __init__(self, id: str, fabric: Fabric) -> None:
        self.fabric = fabric

    @classmethod
    @abstractmethod
    def path_in_parent(cls):
        pass

    @classmethod
    def get_instance(cls, parent, id):
        fabric = parent.fabric.sub([cls.path_in_parent(), id])
        return cls(fabric, id)

    def sync(self, props: List[str] = None):
        """Syncs all props with fabric. if None, syncs all (default)"""
        pass
