def safe_to_enter_next_block(train, next_block_length_m: float, margin_m: float = 25.0) -> bool:
    return train.stopping_distance_m() + margin_m <= next_block_length_m
