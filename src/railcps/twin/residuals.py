def train_residual(payload: dict, twin_state, uncertainty) -> dict[str, float]:
    pos = float(payload.get("position_m", twin_state.position_m))
    speed = float(payload.get("speed_mps", twin_state.speed_mps))
    return {
        "position_z": abs(pos - twin_state.position_m) / max(uncertainty.position_sigma_m, 1e-9),
        "speed_z": abs(speed - twin_state.speed_mps) / max(uncertainty.speed_sigma_mps, 1e-9),
        "block_mismatch": float(str(payload.get("block_id", twin_state.block_id)) != twin_state.block_id),
    }
