from dataclasses import dataclass, field
from .block import Block

@dataclass
class TrackNetwork:
    blocks: dict[str, Block] = field(default_factory=dict)
    adjacency: dict[str, list[str]] = field(default_factory=dict)

    def add_block(self, block: Block, next_blocks: list[str] | None = None) -> None:
        self.blocks[block.block_id] = block
        self.adjacency.setdefault(block.block_id, [])
        if next_blocks is not None:
            self.adjacency[block.block_id] = list(next_blocks)

    def connect(self, a: str, b: str) -> None:
        self.adjacency.setdefault(a, [])
        if b not in self.adjacency[a]:
            self.adjacency[a].append(b)

    def occupy(self, block_id: str, train_id: str) -> None:
        block = self.blocks[block_id]
        if block.occupied_by not in {None, train_id}:
            raise RuntimeError(f"block {block_id} already occupied")
        block.occupied_by = train_id

    def release(self, block_id: str, train_id: str) -> None:
        block = self.blocks[block_id]
        if block.occupied_by == train_id:
            block.occupied_by = None
