from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel

from api.dependancies import get_header_token
from api.exceptions import AlreadyExistsException
from api.models.Token import Token
from api.models.User import UserForCreate, UserForLogin, UserOutput
from api.services import auth_service, user_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class UserData(BaseModel):
    token: Token
    user: UserOutput


@router.get("/me")
async def read_users_me(request: Request) -> UserOutput:
    return auth_service.get_current_user(get_header_token(request))


@router.post("/login")
async def login_for_access_token(
    form_data: UserForLogin,
) -> UserData:
    user_output: UserOutput = auth_service.authenticate_user(
        form_data.email, form_data.password)
    if not user_output:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user_output.email}, expires_delta=access_token_expires
    )
    return UserData(token=Token(access_token=access_token, token_type="Bearer"), user=user_output)


@router.post("/register")
async def register_user(
    user: UserForCreate,
) -> UserData:
    try:
        user_output: UserOutput = user_service.create_user(user)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_output:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="L'utilisateur existe déjà",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user_output.email}, expires_delta=access_token_expires
    )
    return UserData(token=Token(access_token=access_token, token_type="Bearer"), user=user_output)
