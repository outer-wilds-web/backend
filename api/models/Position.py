from pydantic import BaseModel
from datetime import datetime
import uuid


class Position(BaseModel):
    """Represents a position with coordinates and timestamp in ms."""
    id: uuid.UUID
    x: float
    y: float
    z: float
    time: datetime
