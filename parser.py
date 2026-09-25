from typing import Any

def read() -> dict[str,str]:
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

def parse_hub() -> Any:
    
def parse_connection() -> Any:

def set_values(config_dict: dict[str, str]):
    for key in config_dict:
        if config_dict[key] == "start_hub":
            start_hub = Hub()

    

if __name__ == "__main__":
    config_dict: dict[str, str]
    config_dict = read()
    set_values(config_dict)


        
