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
                 actual_nb_drones: int = 0
                 ) -> None:

        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
        self.actual_nb_drones = actual_nb_drones


class Connection():
    def __init__(self,
                 first_hub: str,
                 second_hub: str,
                 max_link_capacity: int = 1) -> None:

        self.first_hub = first_hub
        self.second_hub = second_hub
        self.max_link_capacity = max_link_capacity


class Drone():
    def __init__(self,
                 actual_hub: Hub,
                 turn_to_wait: int) -> None:

        self.actual_hub = actual_hub
        self.turn_to_wait = turn_to_wait


class Map():
    def __init__(self,
                 nb_drones: int = 0,
                 start: Hub | None = None,
                 end: Hub | None = None,
                 hubs: list[Hub] = [],
                 connections: list[Connection] = [],
                 turn_count: int = 0) -> None:

        self.nb_drones = nb_drones
        self.start = start
        self.end = end
        self.hubs = hubs
        self.connections = connections
        self.turn_count = turn_count


class Graph():
    def __init__(self, map: Map) -> None:
        self.map = map
        self.hubs: dict[str, Hub] = {
            hub.name: hub for hub in map.hubs
            }
        self.neighbours: dict[str, list[tuple[str, Connection]]] = {
            name: [] for name in self.hubs
            }
        for connection in map.connections:
            self.neighbours[connection.first_hub].append(
                (connection.second_hub, connection))
            self.neighbours[connection.second_hub].append(
                (connection.first_hub, connection))

    def dfs(self, name: str, visited: set[str] | None = None) -> set[str]:
        """returns every hub reachable from name"""
        if visited is None:
            visited = set()
        visited.add(name)
        # print(name, end=" ")
        for neighbour, _ in self.neighbours[name]:
            if neighbour not in visited and self.hubs[neighbour].zone is not ZoneType.BLOCKED:
                self.dfs(neighbour, visited)
        return visited
