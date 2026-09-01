from dataclasses import dataclass, field

@dataclass
class Train:
    train_id: str
    route: list[str]
    speed_mps: float = 0.0
    max_speed_mps: float = 22.0
    accel_mps2: float = 0.8
    brake_mps2: float = 1.2
    route_index: int = 0
    progress_m: float = 0.0
    completed: bool = False
    stopped_s: float = 0.0
    history: list[tuple[float, str, float]] = field(default_factory=list)

    @property
    def block_id(self) -> str:
        return self.route[min(self.route_index, len(self.route)-1)]

    def step_speed(self, target_mps: float, dt: float) -> None:
        target = max(0.0, min(self.max_speed_mps, target_mps))
        if target > self.speed_mps:
            self.speed_mps = min(target, self.speed_mps + self.accel_mps2 * dt)
        else:
            self.speed_mps = max(target, self.speed_mps - self.brake_mps2 * dt)

    def stopping_distance_m(self) -> float:
        if self.brake_mps2 <= 0:
            return float("inf")
        return self.speed_mps ** 2 / (2 * self.brake_mps2)
