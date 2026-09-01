from dataclasses import dataclass

@dataclass
class TwinUncertainty:
    position_sigma_m: float = 25.0
    speed_sigma_mps: float = 2.0
