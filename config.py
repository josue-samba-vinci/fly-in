from enum import Enum
from heapq import heapify, heappop, heappush


class ZoneType(Enum):
    """Enumerate class that represents every types of zones"""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def cost(self) -> int:
        return 2 if self is ZoneType.RESTRICTED else 1


class Hub():
    """Class representing a hub inside a map"""
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
    """Class representing a connection inside a map"""
    def __init__(self,
                 first_hub: str,
                 second_hub: str,
                 max_link_capacity: int = 1) -> None:

        self.first_hub = first_hub
        self.second_hub = second_hub
        self.max_link_capacity = max_link_capacity


class Drone():
    """Class representing a drone inside a map"""
    def __init__(self,
                 actual_hub: Hub,
                 id: int,
                 path: list[str]
                 ) -> None:

        self.actual_hub = actual_hub
        self.id = id
        self.path = path


class Map():
    """Class representing the map"""
    def __init__(self,
                 nb_drones: int,
                 start: Hub,
                 end: Hub,
                 hubs: list[Hub] = [],
                 connections: list[Connection] = [],
                 turn_count: int = 0) -> None:

        self.nb_drones = nb_drones
        self.start = start
        self.end = end
        self.hubs = hubs
        self.connections = connections
        self.turn_count = turn_count

    def create_drones(self) -> list[Drone]:
        """returns a list of drones contained in the map"""
        drones: list[Drone] = []
        for i in range(1, self.nb_drones + 1):
            drones.append(Drone(self.start, i, []))
        return drones


class Graph():
    """Class representing the graph (map + drones)"""
    def __init__(self, map: Map) -> None:
        self.map = map
        self.hubs: dict[str, Hub] = {
            hub.name: hub for hub in map.hubs
            }
        self.graph: dict[str, list[tuple[str, int]]] = {
            name: [] for name in self.hubs
            }
        self.drones: list[Drone] = []
        for connection in map.connections:
            self.graph[connection.first_hub].append(
                (connection.second_hub,
                 self.hubs[connection.second_hub].zone.cost()))
            self.graph[connection.second_hub].append(
                (connection.first_hub,
                 self.hubs[connection.first_hub].zone.cost()))

    def set_distances(self, source: str) -> dict[str, float]:
        """sets distances of every node to inf and 0 for the source node"""
        distances = {node: float("inf") for node in self.graph}
        distances[source] = 0
        return distances

    def shortest_path(self, source: str, end: str) -> list[str]:
        """returns the shortest path from source to end"""
        distances: dict[str, float] = self.set_distances(source)
        pq = [(0, source)]
        heapify(pq)
        best_previous: dict[str, str] = {}
        visited = set()
        while pq:
            current_distance, current_node = heappop(pq)
            if current_node in visited:
                continue
            visited.add(current_node)
            for neighbor, distance in self.graph[current_node]:
                non_final_distance = current_distance + distance
                if (non_final_distance < distances[neighbor]
                   and self.hubs[neighbor].zone is not ZoneType.BLOCKED):
                    distances[neighbor] = non_final_distance
                    best_previous[neighbor] = current_node
                    heappush(pq, (non_final_distance, neighbor))
        path: list[str] = []
        path.append(end)
        temp_key = end
        while (temp_key != source):
            temp_key = best_previous[temp_key]
            path.append(temp_key)
        return path[::-1]

    def dfs(self, name: str, visited: list[str] | None = None) -> list[str]:
        """returns every hub reachable from name"""
        if visited is None:
            visited = []
        visited.append(name)
        for neighbour, _ in self.graph[name]:
            if (neighbour not in visited and
               self.hubs[neighbour].zone is not ZoneType.BLOCKED):
                self.dfs(neighbour, visited)
        return visited

    def get_hub(self, hub_name: str) -> Hub:
        if hub_name not in self.hubs:
            raise ValueError(f"{hub_name} hub doesn't exist")
        return self.hubs[hub_name]
