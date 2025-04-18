from typing import Optional

from pydantic import BaseModel, PositiveInt


class Shot(BaseModel):
    project: str
    name: Optional[str]
    frame_start: PositiveInt
    frame_end: PositiveInt
    renumber: Optional[int]
