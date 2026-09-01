from dataclasses import dataclass, field
from .telemetry import TelemetryPacket

@dataclass
class FreshnessChecker:
    last_sequence: dict[str, int] = field(default_factory=dict)
    last_timestamp: dict[str, float] = field(default_factory=dict)

    def check(self, packet: TelemetryPacket) -> dict[str, bool]:
        seq_bad = packet.sequence <= self.last_sequence.get(packet.source, -1)
        time_bad = packet.timestamp <= self.last_timestamp.get(packet.source, float("-inf"))
        self.last_sequence[packet.source] = max(packet.sequence, self.last_sequence.get(packet.source, -1))
        self.last_timestamp[packet.source] = max(packet.timestamp, self.last_timestamp.get(packet.source, float("-inf")))
        return {"sequence_stale": seq_bad, "timestamp_stale": time_bad}
