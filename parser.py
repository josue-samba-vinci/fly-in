from config import Hub, Connection, Map, ZoneType
import sys


def get_map() -> Map:
    """parse a map file into a Map object"""
    line_number: int = 0
    content: str
    nb_drones: int = 0
    start: Hub = None
    end: Hub = None
    hubs: list[Hub] = []
    connections: list[Connection] = []
    with open("input.txt", "r") as f:
        content = f.read()
    lines = content.splitlines()
    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        field, sep, body = line.partition(":")
        if not sep or not body or not field:
            raise ValueError("Invalid line")
        try:
            match field:
                case "nb_drones":
                    nb_drones = int(body)
                    line_number += 1
                case "start_hub":
                    hub = parse_hub(body)
                    start = hub
                    hubs.append(hub)
                    line_number += 1
                case "end_hub":
                    hub = parse_hub(body)
                    end = hub
                    hubs.append(hub)
                    line_number += 1
                case "hub":
                    hub = parse_hub(body)
                    hubs.append(hub)
                    line_number += 1
                case "connection":
                    connection = parse_connection(body, hubs)
                    connections.append(connection)
                    line_number += 1
                case _:
                    raise ValueError(f"Invalid field : {field}")
        except ValueError as e:
            print(f"line {line_number} : {e}")
    if nb_drones == 0:
        raise ValueError("nb_drones missing or equal 0")
    elif start is None:
        raise ValueError("start missing")
    elif end is None:
        raise ValueError("end missing")
    elif len(hubs) == 0:
        raise ValueError("no hubs")
    elif len(connections) == 0:
        raise ValueError("no connections")
    return Map(nb_drones, start, end, hubs, connections)


def parse_metadata(metadata: str) -> dict[str, str]:
    "parse a [key=value,...] block into a dict"
    metadata = metadata.strip()
    if not metadata.startswith("[") or not metadata.endswith("]"):
        raise ValueError("invalid metadata block")
    metadata_dict: dict[str, str] = {}
    for data in metadata[1:-1].split():
        key, sep, value = data.partition("=")
        if not sep or not key or not value:
            raise ValueError(f"invalid metadata part : {data}")
        metadata_dict[key] = value
    return metadata_dict


def parse_hub(line: str) -> Hub:
    """receives the values of a hub and transforms it into a Hub object"""
    head, sep, rest = line.partition("[")
    values = head.split()
    if len(values) != 3:
        raise ValueError("a hub needs a name and two coordinates")
    metadata = parse_metadata(sep + rest) if sep else {}
    return Hub(
            name=values[0],
            pos_x=int(values[1]),
            pos_y=int(values[2]),
            zone=ZoneType(metadata.get("zone", "normal")),
            color=metadata.get("color"),
            max_drones=int(metadata.get("max_drones", 1))
               )


def parse_connection(line: str, hubs: list[Hub]) -> Connection:
    """receives the value of a connection and transforms it into a Connection
      object"""
    head, sep, rest = line.partition("[")
    values = [field.strip() for field in head.split("-")]
    if len(values) != 2:
        raise ValueError("A connection requires two hubs")
    hub_names = [hub.name for hub in hubs]
    # print(hub_names)
    for hub in values:
        # print("I'm", end="")
        # print(hub)
        if hub not in hub_names:
            raise ValueError(f"{hub} is not an existing hub")
    metadata = parse_metadata(sep + rest) if sep else {}
    return Connection(
                    first_hub=values[0],
                    second_hub=values[1],
                    max_link_capacity=int(metadata.get("max_link_capacity", 1))
                     )


def main() -> int:
    try:
        map: Map = get_map()
        print(f"nb_drones : {map.nb_drones}")
        start = map.start
        print("start : ", end="")
        print(f"{start.color}, ", end="")
        print(f"{start.name}, ", end="")
        print(f"{start.pos_x}, ", end="")
        print(f"{start.pos_y}, ", end="")
        print(start.zone)
        end = map.end
        print("end : ", end="")
        print(f"{end.color}, ", end="")
        print(f"{end.name}, ", end="")
        print(f"{end.pos_x}, ", end="")
        print(f"{end.pos_y}, ", end="")
        print(end.zone)
        nb = 1
        for hub in map.hubs:
            print(f"hub {nb}: ", end="")
            print(f"{hub.name}, ", end="")
            print(f"{hub.pos_x}, ", end="")
            print(f"{hub.pos_y}, ", end="")
            print(f"{hub.color}, ", end="")
            print(hub.zone)
            nb += 1
        nb = 1
        for connection in map.connections:
            print(f"connection {nb}: ", end="")
            print(f"{connection.first_hub}, ", end="")
            print(f"{connection.second_hub}, ", end="")
            print(f"{connection.max_link_capacity}")
            nb += 1
    except (ValueError, AttributeError) as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    main()
