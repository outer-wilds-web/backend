from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    type_object: str
    name: str
    x: float
    y: float
    z: float
    timestamp: int
