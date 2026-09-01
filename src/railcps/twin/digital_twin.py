from dataclasses import dataclass, field

@dataclass
class TwinTrainState:
    block_id: str
    position_m: float
    speed_mps: float

@dataclass
class RailwayDigitalTwin:
    states: dict[str, TwinTrainState] = field(default_factory=dict)
    block_length_m: float = 300.0
    accel_mps2: float = 0.8
    brake_mps2: float = 1.2

    def initialize(self, train) -> None:
        self.states[train.train_id] = TwinTrainState(train.block_id, train.progress_m, train.speed_mps)

    def predict(self, train_id: str, route: list[str], target_speed_mps: float, dt: float) -> TwinTrainState:
        s = self.states[train_id]
        target = max(0.0, min(22.0, target_speed_mps))
        if target > s.speed_mps:
            speed = min(target, s.speed_mps + self.accel_mps2 * dt)
        else:
            speed = max(target, s.speed_mps - self.brake_mps2 * dt)
        pos = s.position_m + speed * dt
        block = s.block_id
        while pos >= self.block_length_m:
            idx = route.index(block) if block in route else 0
            if idx >= len(route)-1:
                pos = self.block_length_m
                speed = 0.0
                break
            pos -= self.block_length_m
            block = route[idx+1]
        self.states[train_id] = TwinTrainState(block, pos, speed)
        return self.states[train_id]
