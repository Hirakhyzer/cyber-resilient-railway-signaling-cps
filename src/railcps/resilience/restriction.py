def restricted_speed(normal_speed_mps: float, trust: float, safety_conflict: bool) -> float:
    if safety_conflict:
        return 0.0
    if trust < 0.3:
        return min(normal_speed_mps, 4.0)
    if trust < 0.6:
        return min(normal_speed_mps, 8.0)
    return normal_speed_mps
