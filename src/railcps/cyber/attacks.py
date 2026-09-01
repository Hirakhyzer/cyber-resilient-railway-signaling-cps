from dataclasses import dataclass, field
from .telemetry import TelemetryPacket

@dataclass
class AttackInjector:
    mode: str = "none"
    target: str | None = None
    magnitude: float = 0.0
    replay_buffer: TelemetryPacket | None = None
    frozen: TelemetryPacket | None = None

    def apply(self, packet: TelemetryPacket, step: int, active: bool) -> TelemetryPacket:
        p = packet.clone()
        if self.replay_buffer is None:
            self.replay_buffer = p.clone()
        if not active or self.mode == "none":
            if step % 5 == 0:
                self.replay_buffer = p.clone()
            self.frozen = None
            return p
        if self.target and p.source != self.target:
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
        elif self.mode == "replay" and self.replay_buffer is not None:
            p = self.replay_buffer.clone()
        elif self.mode == "rewritten_replay" and self.replay_buffer is not None:
            old = self.replay_buffer.clone()
            old.sequence = packet.sequence
            old.timestamp = packet.timestamp
            p = old
        elif self.mode == "freeze":
            if self.frozen is None:
                self.frozen = p.clone()
            p = self.frozen.clone()
        return p
