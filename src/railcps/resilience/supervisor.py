from dataclasses import dataclass

@dataclass
class ResilienceDecision:
    state: str
    speed_cap_mps: float

class ResilienceSupervisor:
    def decide(self, trust: float, alarm: bool, safety_conflict: bool, recovered: bool) -> ResilienceDecision:
        if safety_conflict:
            return ResilienceDecision("SAFE_STOP", 0.0)
        if alarm and trust < 0.45:
            return ResilienceDecision("ISOLATE_SOURCE", 4.0)
        if alarm:
            return ResilienceDecision("DIAGNOSE", 8.0)
        if recovered and trust < 0.8:
            return ResilienceDecision("RECOVERY", 10.0)
        if trust < 0.7:
            return ResilienceDecision("RESTRICT_OPERATION", 10.0)
        return ResilienceDecision("NORMAL", 22.0)
