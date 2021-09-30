from typing import Any, Dict, List, Optional

from dataclasses import dataclass
from ucel.fabic import NestedFabric
import enum

class ComputeState(enum.Enum):
    QUEUED = enum.auto()
    STARTING = enum.auto()
    RUNNING = enum.auto()
    FAILED = enum.auto()
    ENDED = enum.auto()

@dataclass
class Connectivity:
    hostname: str
    ip: str
    network: str


@dataclass
class Compute(NestedFabric):
    slices: List[slice]
    connectivity: Connectivity
