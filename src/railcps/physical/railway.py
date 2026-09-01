from dataclasses import dataclass, field
from .track import TrackNetwork
from .train import Train
from .signal import Signal
from .switch import Switch

@dataclass
class Railway:
    track: TrackNetwork
    trains: dict[str, Train] = field(default_factory=dict)
    signals: dict[str, Signal] = field(default_factory=dict)
    switches: dict[str, Switch] = field(default_factory=dict)

    def add_train(self, train: Train) -> None:
        self.trains[train.train_id] = train
        self.track.occupy(train.block_id, train.train_id)

    def move_train(self, train_id: str, target_speed_mps: float, dt: float) -> None:
        train = self.trains[train_id]
        if train.completed:
            return
        train.step_speed(target_speed_mps, dt)
        block = self.track.blocks[train.block_id]
        train.progress_m += train.speed_mps * dt
        while train.progress_m >= block.length_m and not train.completed:
            train.progress_m -= block.length_m
            old = train.block_id
            if train.route_index >= len(train.route)-1:
                train.completed = True
                train.speed_mps = 0.0
                self.track.release(old, train.train_id)
                return
            nxt = train.route[train.route_index+1]
            if not self.track.blocks[nxt].clear:
                train.progress_m = block.length_m - 1e-6
                train.speed_mps = 0.0
                return
            self.track.release(old, train.train_id)
            train.route_index += 1
            self.track.occupy(nxt, train.train_id)
            block = self.track.blocks[nxt]
