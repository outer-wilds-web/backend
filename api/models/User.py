from pydantic import BaseModel, Field
from typing import List

import uuid


class User(BaseModel):
    """Represents a user with roles, hashed password, and other details."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    username: str
    roles: List[str] = Field(default_factory=lambda: ["user"])
    hashed_password: str


class UserOutput(BaseModel):
    """Represents a user output with public details."""
    id: uuid.UUID
    email: str
    username: str
    roles: List[str] = Field(default_factory=lambda: ["user"])


class UserForCreate(BaseModel):
    """Represents the payload for creating a new user."""
    email: str
    password: str
    username: str


class UserForUpdate(BaseModel):
    """Represents the payload for updating user details."""
    email: str
    username: str


class UserForLogin(BaseModel):
    """Represents the payload for user login."""
    email: str
    password: str
