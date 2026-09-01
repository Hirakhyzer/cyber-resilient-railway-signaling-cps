def reported_occupancy(railway) -> dict[str, int]:
    return {bid: int(not block.clear) for bid, block in railway.track.blocks.items()}
