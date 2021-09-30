from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from ucel.status import Action, State, Status
from ucel.fabic import NestedFabric
import enum

@dataclass
class Healthcheck:
    """
    A healtcheck
    """
    test: List[str]
    "the test to run. Exit code of 0 is healthy, 1 is unhealthy, 2 is reserved"
    retries: int = 3
    "If a single run of the check takes longer than timeout seconds then the check is considered to have failed."
    interval: float = 30
    "The health check will first run interval seconds after the container is started, and then again interval seconds after each previous check completes."
    start_period: float = 0
    "failure during that period will not be counted towards the maximum number of retries. However, if a health check succeeds during the start period, the it is considered started and all consecutive failures will be counted towards the maximum number of retries."
    timeout: float = 30
    "If a single run of the check takes longer than timeout seconds then the check is considered to have failed."


class Protocol(enum.Enum):
    TCP = enum.auto()
    UDP = enum.auto()

@dataclass
class Port:
    name: str
    "must be a dns style label with max length 10"

    port: Optional[int] = None
    "what port"

    protocol: Protocol = Protocol.TCP
    "what protocol is talked on port"

    expose: bool = False
    "Should this port be exposed"

    ip: Optional[str] = None
    "What ip to bind to"

@dataclass
class ConnectionConfig:
    ports: List[Port] = {}
    metadata: dict = {}
    def make_connection_file(self):
        "Make a jupyter style connection file"

@dataclass
class Payload:
    cmd: List[str]
    name: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    cwd: Optional[str] = None
    connection_file: Optional[dict] = None
    timeout: Optional[float] = None
    healtcheck: Optional[Healthcheck] = None

@dataclass
class Task(NestedFabric):
    payload: Payload
    action: Optional[Action] = None
    state: State = State()
    connection_file: dict = None
    "connection info output. if Payload has connection_file this is that but with assigned ports"
