from .route_conflicts import conflicting_locked_routes

def evaluate_safety(railway, interlocking) -> dict[str, int]:
    occupied = {}
    duplicate_occupancy = 0
    for tid, train in railway.trains.items():
        if train.completed:
            continue
        if train.block_id in occupied and occupied[train.block_id] != tid:
            duplicate_occupancy += 1
        occupied[train.block_id] = tid
    signal_conflicts = 0
    for signal in railway.signals.values():
        if signal.aspect == "GREEN" and not railway.track.blocks[signal.protects_block].clear:
            signal_conflicts += 1
    return {
        "duplicate_occupancy": duplicate_occupancy,
        "route_conflicts": len(conflicting_locked_routes(interlocking)),
        "signal_conflicts": signal_conflicts,
    }
