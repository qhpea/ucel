from typing import Any, Dict, List, Optional

from dataclasses import dataclass

@dataclass
class Image:
    name: str
    repo: str

@dataclass
class Container(NestedFabric):
    tasks: List[Task] = []
    image: Image = None
