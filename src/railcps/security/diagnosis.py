def diagnose(result, source_kind: str, safety_conflict: bool = False, degraded_network: bool = False) -> str:
    if safety_conflict:
        return "SAFETY_CONFLICT"
    if not result.alarm:
        return "NORMAL"
    if degraded_network and any(r in result.reasons for r in ("sequence_stale", "timestamp_stale")):
        return "COMMUNICATION_FAULT"
    if source_kind in {"occupancy", "signal", "switch", "train"}:
        return "CYBER_ANOMALY"
    return "UNKNOWN"
