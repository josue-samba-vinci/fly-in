from typing import Any
from config import Hub, Connection, Map


def read() -> dict[str, str]:
    """reads the content of an input file and returns a dict cotaining"""
    """every necessary key to build the map with its value"""
    content: str
    lines: list[str]
    config_dict: dict[str, str] = {}
    with open("input.txt", "r") as f:
        content = f.read()
    lines = content.splitlines()
    for line in lines:
        if line.startswith("#") or line.strip == "":
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
    """receives the value of a hub and transforms    it into an Hub object"""
    head, sep, rest = line.partition("[")
    values = head.split()
    if len(values) != 3:
        raise ValueError("a hub needs a name and two coordinates")
    metadata = parse_metadata(sep + rest) if sep else {}
    return Hub(name=values[0],
               pos_x=values[1],
               pos_y=values[2],
               zone=metadata.get("zone"),
               zone=metadata.get("color"),
               zone=metadata.get("max_drones")
               )


# def parse_connection(line: str) -> Connection:


if __name__ == "__main__":
    config_dict: dict[str, str]
    config_dict = read()
    hub1 = parse_hub(config_dict["start_hub"])
    print(hub1)
    # set_values(config_dict)
