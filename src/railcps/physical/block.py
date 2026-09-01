from dataclasses import dataclass

@dataclass
class Block:
    block_id: str
    length_m: float = 500.0
    occupied_by: str | None = None

    @property
    def clear(self) -> bool:
        return self.occupied_by is None
