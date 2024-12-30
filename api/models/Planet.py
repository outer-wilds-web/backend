from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Planet(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str

# il faudra ajouter d'autre parametre, Nom, position dans le systeme, taille ... etc
