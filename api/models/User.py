from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    username: str
    roles: list[str] = ["user"]
    hashed_password: str


class UserOutput(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    roles: list[str] = ["user"]


class UserForCreate(BaseModel):
    email: str
    password: str
    username: str


class UserForUpdate(BaseModel):
    email: str
    username: str


class UserForLogin(BaseModel):
    email: str
    password: str
