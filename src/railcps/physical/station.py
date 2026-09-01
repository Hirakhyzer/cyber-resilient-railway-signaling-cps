from dataclasses import dataclass

@dataclass
class Station:
    station_id: str
    block_id: str
    dwell_s: float = 20.0
