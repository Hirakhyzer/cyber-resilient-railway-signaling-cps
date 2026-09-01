def service_metrics(trains: dict, elapsed_s: float) -> dict[str, float]:
    total=len(trains)
    completed=sum(1 for t in trains.values() if t.completed)
    return {"completion_ratio": completed/total if total else 1.0, "elapsed_s": elapsed_s}
