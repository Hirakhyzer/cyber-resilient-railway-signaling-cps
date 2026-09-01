def movement_authority_blocks(train, railway, lookahead: int = 1) -> int:
    allowed = 0
    for idx in range(train.route_index + 1, min(len(train.route), train.route_index + 1 + lookahead)):
        block = railway.track.blocks[train.route[idx]]
        if not block.clear:
            break
        allowed += 1
    return allowed
