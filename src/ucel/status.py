from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass, Field
from datetime import datetime





class HealthcheckStatus(Enum):
    STARTING = auto()
    HEALTHY = auto()
    UNHEALTHY = auto()


class Action(Enum):
    RESTART = auto()
    STOP = auto()
    REMOVE = auto()
    PAUSE = auto()


def state_error(state, action):
    return Exception(f"{state} invalid for {action}")


class Status(Enum):
    """
    CREATED -> RUNNING
    CREATED -> EXITED
    CREATED -> REMOVING

    RESTARTING -> RUNNING
    RESTARTING -> EXITED

    RUNNING -> DEAD
    RUNNING -> EXITED
    RUNNING -> PAUSED
    RUNNING -> RESTARTING
    RUNNING -> REMOVING

    REMOVING -> DEAD

    PAUSED -> RUNNING

    EXITED -> RESTARTING
    EXITED -> REMOVING
    EXITED -> DEAD



    DEAD -> REMOVING
    """
    CREATED = auto()
    RESTARTING = auto()
    RUNNING = auto()
    REMOVING = auto()
    DEAD = auto()
    PAUSED = auto()
    EXITED = auto()

    def all_next(self):
        if self == Status.CREATED:
            return [
                Status.RUNNING,
                Status.EXITED,
                Status.REMOVING
            ]
        if self == Status.RESTARTING:
            return [
                Status.RUNNING,
                Status.EXITED,
                Status.REMOVING
            ]
        if self == Status.RUNNING:
            return [
                Status.EXITED,
                Status.PAUSED,
                Status.RESTARTING,
                Status.REMOVING,
            ]
        if self == Status.REMOVING:
            return [Status.DEAD]
        if self == Status.DEAD:
            return []
        if self == Status.PAUSED:
            return [
                Status.RUNNING,
                Status.REMOVING
            ]
        if self == Status.EXITED:
            return [
                Status.RESTARTING,
                Status.REMOVING
            ]
        raise Exception("invalid state")

    def is_removeable(self):
        return not self.is_dead() and not self.is_active()
    
    def is_active(self):
        return self in [Status.CREATED, Status.RESTARTING, Status.RUNNING]
    
    def is_dead(self):
        return self == Status.DEAD
    
    def may_start(self):
        "can this state get into running"
        return self.is_active() and self != Status.RUNNING
    
    def next(self, action: Action):
        if action is None:
            if self.may_start():
                return Status.RUNNING
            if self == Status.RUNNING:
                #TODO I guess i solved the halting problem
                return Status.EXITED
        if action == Action.REMOVE:
            if self.is_removeable():
                return self.REMOVING
        if action == Action.STOP:
            if self.is_active():
                return self.EXITED
        if action == Action.PAUSE:
            if self == Status.RUNNING:
                return self.PAUSED
        if action == Action.RESTART:
            if not self.is_dead():
                return self.RESTARTING
        
        raise state_error(state=self, action=action)


@dataclass
class State:
    status: Status = Status.CREATED

    pulse: Optional[datetime] = None

    health: Optional[HealthcheckStatus] = None

    "exit code if avalible"
    exit_code: Optional[int] = None

    "An error message"
    error: Optional[str] = None

    "the id of the process"
    pid: Optional[int] = None

    last_enter: Dict[Status, datetime] = {}
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    @property
    def may_start_on_own(self):
        return self.status in {Status.CREATED, Status.RESTARTING}

    @property
    def paused(self):
        return self.status == Status.PAUSED

    def __str__(self) -> str:
        return
