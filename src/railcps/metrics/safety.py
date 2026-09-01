def safety_metrics(history: list[dict[str,int]]) -> dict[str,int]:
    keys={"duplicate_occupancy","route_conflicts","signal_conflicts"}
    return {k: sum(item.get(k,0) for item in history) for k in keys}
