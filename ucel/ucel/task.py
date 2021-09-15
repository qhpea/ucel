from dataclasses import dataclass
from typing import Any, Dict, List
from ucel.fabic import NestedFabric
import enum


@dataclass
class Payload:
    cmd: List[str]
    name: str = None
    env: Dict[str, str] = None
    cwd: str = None
    connection_file: dict = None


class TaskState(enum.Enum):
    QUEUED = enum.auto()
    STARTING = enum.auto()
    RUNNING = enum.auto()
    FAILED = enum.auto()
    ENDED = enum.auto()

class TaskAction(enum.Enum):
    START = enum.auto()
    STOP = enum.auto()
    TERMINATE = enum.auto()
    DELETE = enum.auto()


@dataclass
class TaskStatus:
    state: TaskState = TaskState.QUEUED
    changed: Dict[TaskState, str] = {}


@dataclass
class Task(NestedFabric):
    payload: Payload
    command: TaskAction = None
    status: TaskStatus = TaskStatus()    
    
    "connection info. will assign ports to anything with value 0"
    connection_file: dict = None
    stdout: str = None
    stdin: str = None
    sterror: str = None
