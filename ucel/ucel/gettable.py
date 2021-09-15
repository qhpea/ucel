def get(id):
    """Find something by it's id"""
    pass

def register(cls, name = None, parent = None):
    """Register type to be gettable"""
    pass

from abc import ABC, abstractmethod
from typing import Any

class Nested(ABC):
    id: str
    parent: Any
    
    @classmethod
    @abstractmethod
    def get_instance(cls, parent, id):
        pass

    @abstractmethod
    def get_children(self) -> list:
        pass
