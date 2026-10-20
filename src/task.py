"""Shared Task type for both schedulers.

Convention: a LOWER priority number runs FIRST (1 = most urgent).
Tasks with equal priority run in the order they were added (FIFO).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    name: str
    priority: int

    def __post_init__(self):
        if not isinstance(self.priority, int):
            raise TypeError("priority must be an int")
        if not self.name:
            raise ValueError("task name cannot be empty")
