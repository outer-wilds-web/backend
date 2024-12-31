from pydantic import BaseModel, Field
import uuid


class Ship(BaseModel):
    """Represents a ship with a unique identifier, owner, and name."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner: uuid.UUID
    name: str


class ShipForCreate(BaseModel):
    """Represents the payload for creating a new ship."""
    owner: uuid.UUID
    name: str
