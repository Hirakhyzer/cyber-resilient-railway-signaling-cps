from dataclasses import dataclass

@dataclass
class Switch:
    switch_id: str
    position: str = "STRAIGHT"

    def set_position(self, position: str) -> None:
        if position not in {"STRAIGHT", "DIVERGE"}:
            raise ValueError("invalid switch position")
        self.position = position
