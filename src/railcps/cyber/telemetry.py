from dataclasses import dataclass

@dataclass
class TelemetryPacket:
    source: str
    sequence: int
    timestamp: float
    payload: dict[str, float | int | str]

    def clone(self) -> "TelemetryPacket":
        return TelemetryPacket(self.source, self.sequence, self.timestamp, dict(self.payload))
