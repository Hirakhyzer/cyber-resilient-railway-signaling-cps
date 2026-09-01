from dataclasses import dataclass

@dataclass(frozen=True)
class TimetableEntry:
    train_id: str
    planned_finish_s: float
