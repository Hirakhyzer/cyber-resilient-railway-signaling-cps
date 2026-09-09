from dataclasses import dataclass, field
import random
from .telemetry import TelemetryPacket

@dataclass
class Network:
    loss_prob: float = 0.0
    base_delay_s: float = 0.0
    jitter_s: float = 0.0
    rng: random.Random = field(default_factory=random.Random)
    queue: list[tuple[float, TelemetryPacket]] = field(default_factory=list, init=False)

    def _delay_s(self) -> float:
        jitter = self.rng.uniform(-self.jitter_s, self.jitter_s) if self.jitter_s else 0.0
        return max(0.0, self.base_delay_s + jitter)

    def send(self, packet: TelemetryPacket, now_s: float) -> bool:
        """Schedule a packet for simulated delivery.

        Returns ``False`` when the packet is dropped. Delay and jitter affect the
        actual receive time rather than being returned as unused metadata.
        """
        if self.rng.random() < self.loss_prob:
            return False
        self.queue.append((float(now_s) + self._delay_s(), packet))
        return True

    def receive(self, now_s: float) -> list[TelemetryPacket]:
        ready = sorted(
            ((t, p) for t, p in self.queue if t <= float(now_s)),
            key=lambda item: item[0],
        )
        self.queue = [(t, p) for t, p in self.queue if t > float(now_s)]
        return [p for _, p in ready]

    def transmit(self, packet: TelemetryPacket) -> tuple[TelemetryPacket | None, float]:
        """Legacy one-shot API retained for compatibility.

        New simulations should use :meth:`send` and :meth:`receive` so latency is
        applied to packet arrival. This method reports the sampled delay but does
        not itself advance simulated time.
        """
        if self.rng.random() < self.loss_prob:
            return None, 0.0
        return packet, self._delay_s()
