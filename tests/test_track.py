from railcps.physical.block import Block
from railcps.physical.track import TrackNetwork

def test_block_occupancy():
    t=TrackNetwork(); t.add_block(Block("B")); t.occupy("B","T1"); assert not t.blocks["B"].clear; t.release("B","T1"); assert t.blocks["B"].clear
