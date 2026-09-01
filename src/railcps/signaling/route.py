from dataclasses import dataclass, field

@dataclass(frozen=True)
class Route:
    route_id: str
    blocks: tuple[str, ...]
    required_switches: tuple[tuple[str, str], ...] = ()
    conflicts: frozenset[str] = field(default_factory=frozenset)
