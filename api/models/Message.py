from pydantic import BaseModel


class Message(BaseModel):
    """Represents a Kafka message with object type, coordinates, and timestamp."""
    type_object: str
    name: str
    x: float
    y: float
    z: float
    timestamp: int
