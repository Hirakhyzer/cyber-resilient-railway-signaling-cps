from dataclasses import dataclass, field

@dataclass
class RecoveryTracker:
    healthy_steps: dict[str, int] = field(default_factory=dict)

    def update(self, source: str, alarm: bool, required_healthy: int = 5) -> bool:
        if alarm:
            self.healthy_steps[source] = 0
            return False
        self.healthy_steps[source] = self.healthy_steps.get(source, 0) + 1
        return self.healthy_steps[source] >= required_healthy
