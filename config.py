from pydantic import BaseModel, Field, Optional


class Config():
    def __init__(self) -> None:
        start: Hub
        end: Hub
        hubs: list[Hub]
        connections: list[Connection]


class Hub(BaseModel):
    def __init__(self) -> None:
        name: str = Field(min_length=1)
        pos_x: int = Field(ge=0)
        pos_y: int = Field(ge=0)
        color: Optional[str] = Field(min_length=1)


class Connection(BaseModel):
    def __init__(self) -> None:
        first_hub: str
        second_hub: str

        
