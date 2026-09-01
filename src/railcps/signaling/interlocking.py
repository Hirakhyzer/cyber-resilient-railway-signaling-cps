from dataclasses import dataclass, field
from .route import Route
from railcps.physical.railway import Railway

@dataclass
class Interlocking:
    railway: Railway
    routes: dict[str, Route]
    locked: set[str] = field(default_factory=set)

    def can_lock(self, route_id: str, for_train: str | None = None) -> bool:
        route = self.routes[route_id]
        for locked_id in self.locked:
            locked = self.routes[locked_id]
            if locked_id in route.conflicts or route_id in locked.conflicts or set(route.blocks) & set(locked.blocks):
                return False
        for block_id in route.blocks:
            occ = self.railway.track.blocks[block_id].occupied_by
            if occ is not None and occ != for_train:
                return False
        for switch_id, pos in route.required_switches:
            if self.railway.switches[switch_id].position != pos:
                return False
        return True

    def lock(self, route_id: str, for_train: str | None = None) -> bool:
        if not self.can_lock(route_id, for_train=for_train):
            return False
        self.locked.add(route_id)
        return True

    def release(self, route_id: str) -> None:
        self.locked.discard(route_id)
