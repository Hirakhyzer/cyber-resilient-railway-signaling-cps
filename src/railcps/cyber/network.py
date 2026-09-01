from dataclasses import dataclass, field
import random
from .telemetry import TelemetryPacket

@dataclass
class Network:
    loss_prob: float = 0.0
    base_delay_s: float = 0.0
    jitter_s: float = 0.0
    rng: random.Random = field(default_factory=random.Random)

    def transmit(self, packet: TelemetryPacket) -> tuple[TelemetryPacket | None, float]:
        if self.rng.random() < self.loss_prob:
            return None, 0.0
        jitter = self.rng.uniform(-self.jitter_s, self.jitter_s) if self.jitter_s else 0.0
        return packet, max(0.0, self.base_delay_s + jitter)
