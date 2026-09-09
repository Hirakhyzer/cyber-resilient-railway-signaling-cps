from dataclasses import dataclass, field
from .telemetry import TelemetryPacket

@dataclass
class AttackInjector:
    mode: str = "none"
    target: str | None = None
    magnitude: float = 0.0
    replay_buffers: dict[str, TelemetryPacket] = field(default_factory=dict)
    frozen_packets: dict[str, TelemetryPacket] = field(default_factory=dict)

    def apply(self, packet: TelemetryPacket, step: int, active: bool) -> TelemetryPacket:
        p = packet.clone()
        source = p.source
        if source not in self.replay_buffers:
            self.replay_buffers[source] = p.clone()
        if not active or self.mode == "none":
            if step % 5 == 0:
                self.replay_buffers[source] = p.clone()
            self.frozen_packets.pop(source, None)
            return p
        if self.target and source != self.target:
            return p
        if self.mode == "position_spoof":
            p.payload["position_m"] = float(p.payload.get("position_m", 0.0)) + self.magnitude
        elif self.mode == "velocity_spoof":
            p.payload["speed_mps"] = float(p.payload.get("speed_mps", 0.0)) + self.magnitude
        elif self.mode == "occupancy_spoof":
            p.payload["occupied"] = 1 - int(p.payload.get("occupied", 0))
        elif self.mode == "signal_falsification":
            p.payload["aspect"] = "GREEN" if p.payload.get("aspect") != "GREEN" else "RED"
        elif self.mode == "switch_falsification":
            p.payload["position"] = "DIVERGE" if p.payload.get("position") != "DIVERGE" else "STRAIGHT"
        elif self.mode == "replay":
            p = self.replay_buffers[source].clone()
        elif self.mode == "rewritten_replay":
            old = self.replay_buffers[source].clone()
            old.sequence = packet.sequence
            old.timestamp = packet.timestamp
            p = old
        elif self.mode == "freeze":
            if source not in self.frozen_packets:
                self.frozen_packets[source] = p.clone()
            p = self.frozen_packets[source].clone()
        return p
