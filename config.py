from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def cost(self) -> int:
        return 2 if self is ZoneType.RESTRICTED else 1


class Hub():
    def __init__(self,
                 name: str,
                 pos_x: int,
                 pos_y: int,
                 zone: ZoneType = ZoneType.NORMAL,
                 color: str | None = None,
                 max_drones: int = 1,
                 ) -> None:

        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class Connection():
    def __init__(self,
                 first_hub: str,
                 second_hub: str,
                 max_link_capacity: int = 1) -> None:

        self.first_hub = first_hub
        self.second_hub = second_hub
        self.max_link_capacity = max_link_capacity


class Map():
    def __init__(self,
                 nb_drones: int | None = None,
                 start: Hub | None = None,
                 end: Hub | None = None,
                 hubs: list[Hub] | None = None,
                 connections: list[Connection] | None = None) -> None:

        self.nb_drones = nb_drones
        self.start = start
        self.end = end
        self.hubs = hubs
        self.connections = connections
