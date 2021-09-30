
from abc import ABC, abstractmethod
from typing import Any

def get(id):
    """Find something by it's id"""
    pass

def register(cls, name = None, parent = None):
    """Register type to be gettable"""
    pass

class Getable(ABC):
    id: str
    parent: Any
    
    def __init__(self, parent, id) -> None:
        self.id = id
        self.parent = parent
        super().__init__()

    @classmethod
    @abstractmethod
    def path_in_parent(cls):
        "get the name of this"

    @classmethod
    @abstractmethod
    def get_instance(cls, parent, id):
        "get instance of a class from a username and"
        return cls(parent, id)