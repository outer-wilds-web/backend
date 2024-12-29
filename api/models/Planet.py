from pydantic import BaseModel
from datetime import datetime
import uuid


class Planet(BaseModel):
    id: uuid.UUID

# il faudra ajouter d'autre parametre, Nom, position dans le systeme, taille ... etc
