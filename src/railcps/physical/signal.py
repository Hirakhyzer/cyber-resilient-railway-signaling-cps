from dataclasses import dataclass

@dataclass
class Signal:
    signal_id: str
    protects_block: str
    aspect: str = "RED"

    def set_aspect(self, aspect: str) -> None:
        if aspect not in {"RED", "YELLOW", "GREEN"}:
            raise ValueError("invalid signal aspect")
        self.aspect = aspect
