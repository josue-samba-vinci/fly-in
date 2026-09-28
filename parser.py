from config import Hub, Connection, Map


def read() -> dict[str, str]:
    """reads the content of an input file and returns a dict containing
      every necessary key to build the map with its value"""
    content: str
    lines: list[str]
    config_dict: dict[str, str] = {}
    with open("input.txt", "r") as f:
        content = f.read()
    lines = content.splitlines()
    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split(": ")
        if len(parts) > 2 or len(parts) < 2:
            raise ValueError("recheck the input.txt")
        else:
            config_dict.update({parts[0]: parts[1]})
    print(config_dict)
    return config_dict


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
    return Hub(name=values[0],
               pos_x=values[1],
               pos_y=values[2],
               zone=metadata.get("zone", "normal"),
               color=metadata.get("color"),
               max_drones=metadata.get("max_drones", 1)
               )


def parse_connection(line: str, hubs: list[Hub]) -> Connection:
    """receives the value of a connection and transforms it into a Connection
      object"""
    head, sep, rest = line.partition("[")
    values = head.split("-")
    if len(values) != 2:
        raise ValueError("A connection requires two hubs")
    for hub in values:
        if hub not in hubs:
            raise ValueError(f"{hub} is not an existing hub")
    metadata = parse_metadata(sep + rest) if sep else {}
    return Connection(first_hub=values[0],
                      second_hub=values[1],
                      max_link_capacity=metadata.get("max_link_capacity"))

# def get_map()


if __name__ == "__main__":
    config_dict: dict[str, str]
    config_dict = read()
    start = parse_hub(config_dict["start_hub"])
    print("start : ", end="")
    print(f"{start.color}, ", end="")
    print(f"{start.name}, ", end="")
    print(f"{start.pos_x}, ", end="")
    print(f"{start.pos_y}, ", end="")
    print(start.zone)
    end = parse_hub(config_dict["end_hub"])
    print("end : ", end="")
    print(f"{end.color}, ", end="")
    print(f"{end.name}, ", end="")
    print(f"{end.pos_x}, ", end="")
    print(f"{end.pos_y}, ", end="")
    print(end.zone)
