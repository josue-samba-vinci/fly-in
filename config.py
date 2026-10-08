from enum import Enum
from heapq import heapify, heappop, heappush


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
        # print(self.hubs)
        self.graph: dict[str, list[tuple[str, int]]] = {
            name: [] for name in self.hubs
            }
        for connection in map.connections:
            # print(connection.first_hub)
            # print(connection.second_hub)
            self.graph[connection.first_hub].append(
                (connection.second_hub, self.hubs[connection.second_hub].zone.cost()))
            self.graph[connection.second_hub].append(
                (connection.first_hub, self.hubs[connection.first_hub].zone.cost()))
        print(self.graph)

    def set_distances(self, source: str) -> dict[str, int]:
        distances = {node: float("inf") for node in self.graph}
        distances[source] = 0
        return distances
        # print(distances)

    def shortest_path(self, source: str):
        distances: dict[str, float] = self.set_distances(source)
        pq = [(0, source)]
        heapify(pq)
        visited = set()
        while pq:
            print(f"pq : {pq}")
            current_distance, current_node = heappop(pq)
            print(f"current_distance : {current_distance}")
            print(f"current_node : {current_node}")
            print(f"visited : {visited}")
            if current_node in visited:
                continue
            visited.add(current_node)
            for neighbor, distance in self.graph[current_node]:
                print(f"CHECK DES DISTANCES DE {neighbor}")
                non_final_distance = current_distance + distance
                print(f"non_final_distance : {non_final_distance}")
                print(f"distances[{neighbor}] : {distances[neighbor]}")
                if non_final_distance < distances[neighbor]:
                    print(f"MISE A JOUR DE LA DISTANCE DANS DISTANCES[{neighbor}]")
                    distances[neighbor] = non_final_distance
                    heappush(pq, (non_final_distance, neighbor))
        return distances

    def dfs(self, name: str, visited: list[str] | None = None) -> list[str]:
        """returns every hub reachable from name"""
        # breakpoint()
        if visited is None:
            visited = []
        visited.append(name)
        # print(f"visited = {visited}")
        # print(name, end=" ")
        for neighbour, _ in self.graph[name]:
            # print(f"neighbour = {neighbour}")
            if (neighbour not in visited and
               self.hubs[neighbour].zone is not ZoneType.BLOCKED):
                self.dfs(neighbour, visited)
        # print(f"{neighbour}")
        # print(visited)
        return visited

    def dijkstra(self, name: str, path: list[str] | None = None) -> list[str]:
        if path is None:
            path = []
        path.append(name)
