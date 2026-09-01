from dataclasses import dataclass, field

@dataclass
class TrustManager:
    scores: dict[str, float] = field(default_factory=dict)

    def get(self, source: str) -> float:
        return self.scores.get(source, 1.0)

    def update(self, source: str, anomaly_score: float) -> float:
        current = self.get(source)
        if anomaly_score >= 1.0:
            current = max(0.0, current - min(0.35, 0.08 * anomaly_score))
        else:
            current = min(1.0, current + 0.02)
        self.scores[source] = current
        return current
