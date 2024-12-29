from pydantic import BaseModel, Field
import uuid


class Ship(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner: uuid.UUID


class ShipForCreate(BaseModel):
    owner: uuid.UUID
