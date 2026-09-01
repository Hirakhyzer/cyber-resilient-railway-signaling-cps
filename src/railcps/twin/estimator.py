def reconstruct_train_state(twin_state, payload: dict, trust: float) -> dict:
    if trust < 0.5:
        return {"block_id": twin_state.block_id, "position_m": twin_state.position_m, "speed_mps": twin_state.speed_mps}
    return {
        "block_id": str(payload.get("block_id", twin_state.block_id)),
        "position_m": float(payload.get("position_m", twin_state.position_m)),
        "speed_mps": float(payload.get("speed_mps", twin_state.speed_mps)),
    }
