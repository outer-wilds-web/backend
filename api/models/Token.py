from pydantic import BaseModel


class Token(BaseModel):
    """Represents an access token for authentication."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Represents token data containing user email."""
    email: str
