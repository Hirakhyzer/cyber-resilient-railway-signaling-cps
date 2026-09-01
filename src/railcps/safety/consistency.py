def occupancy_consistency(train_payload: dict, occupancy_payload: dict) -> bool:
    block_id = str(train_payload.get("block_id", ""))
    if str(occupancy_payload.get("block_id", "")) != block_id:
        return True
    return int(occupancy_payload.get("occupied", 0)) == 1
