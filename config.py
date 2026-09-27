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
                 color: str | None = None) -> None:

        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color


class Connection():
    def __init__(self,
                 first_hub: str,
                 second_hub: str) -> None:

        self.first_hub = first_hub
        self.second_hub = second_hub


class Map():
    def __init__(self,
                 start: Hub,
                 end: Hub,
                 hubs: list[Hub],
                 connections: list[Connection]) -> None:

        self.start = start
        self.end = end
        self.hubs = hubs
        self.connections = connections
