"""
Components are data structures which hold data that systems read from and write to. Any data that
a system depends on should be defined here.
"""

from dataclasses import dataclass, field

from .actions import ActionEmitter, ActionValue


@dataclass
class BoxComponent:
    width: int
    height: int


@dataclass
class ActionEmitterComponent:
    action_emitter: ActionEmitter
    actions: list[ActionValue] = field(default_factory=list[ActionValue])


@dataclass
class MovementComponent:
    pass


@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0
