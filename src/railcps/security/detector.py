from dataclasses import dataclass

@dataclass
class DetectionResult:
    source: str
    score: float
    alarm: bool
    reasons: tuple[str, ...]

class HybridDetector:
    def __init__(self, threshold: float = 2.5):
        self.threshold = threshold

    def evaluate_train(self, source: str, residual: dict[str, float], freshness: dict[str, bool], invariant_penalty: float = 0.0) -> DetectionResult:
        reasons=[]
        score=max(residual.get("position_z",0.0), residual.get("speed_z",0.0), 2.5*residual.get("block_mismatch",0.0))
        if residual.get("position_z",0.0) >= self.threshold: reasons.append("position_residual")
        if residual.get("speed_z",0.0) >= self.threshold: reasons.append("speed_residual")
        if residual.get("block_mismatch",0.0): reasons.append("block_mismatch")
        if freshness.get("sequence_stale"): score += 2.5; reasons.append("sequence_stale")
        if freshness.get("timestamp_stale"): score += 2.5; reasons.append("timestamp_stale")
        if invariant_penalty: score += invariant_penalty; reasons.append("safety_invariant")
        return DetectionResult(source, score, score >= self.threshold, tuple(reasons))

    def evaluate_discrete(self, source: str, expected: dict, payload: dict, freshness: dict[str,bool]) -> DetectionResult:
        mismatches=sum(1 for k,v in expected.items() if payload.get(k)!=v)
        score=3.0*mismatches
        reasons=[]
        if mismatches: reasons.append("state_mismatch")
        if freshness.get("sequence_stale"): score += 2.5; reasons.append("sequence_stale")
        if freshness.get("timestamp_stale"): score += 2.5; reasons.append("timestamp_stale")
        return DetectionResult(source, score, score >= self.threshold, tuple(reasons))
