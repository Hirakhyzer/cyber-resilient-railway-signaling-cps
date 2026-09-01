def target_speed(train, authority_blocks: int, supervisor_cap_mps: float) -> float:
    if authority_blocks <= 0:
        return 0.0
    return min(train.max_speed_mps, supervisor_cap_mps)
