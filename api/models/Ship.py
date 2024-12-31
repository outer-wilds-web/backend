from pydantic import BaseModel, Field
import uuid


class Ship(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner: uuid.UUID
    name: str


class ShipForCreate(BaseModel):
    owner: uuid.UUID
    name: str
