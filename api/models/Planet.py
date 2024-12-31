from pydantic import BaseModel, Field
import uuid


class Planet(BaseModel):
    """Represents a planet with a unique identifier and name."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
