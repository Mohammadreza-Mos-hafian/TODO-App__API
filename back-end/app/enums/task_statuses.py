from enum import Enum


class TaskStatus(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    CANCELED = 3
