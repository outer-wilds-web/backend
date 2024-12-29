from pydantic import BaseModel
from datetime import datetime
import uuid


class Position(BaseModel):
    id : uuid.UUID
    x: float
    y: float
    z: float
    time : datetime