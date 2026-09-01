def resilience_score(completed_ratio: float, safety_violations: int, restriction_fraction: float) -> float:
    if safety_violations > 0:
        return 0.0
    return max(0.0, min(1.0, completed_ratio * (1.0 - 0.5*restriction_fraction)))
