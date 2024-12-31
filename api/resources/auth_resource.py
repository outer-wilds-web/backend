from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel
from config.config import get_logger

from api.dependancies import get_header_token
from api.exceptions import AlreadyExistsException
from api.models.Token import Token
from api.models.User import UserForCreate, UserForLogin, UserOutput
from api.services import auth_service, user_service

logger = get_logger()

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class UserData(BaseModel):
    """Represents the data returned after authentication or registration.

    Attributes:
        token (Token): The access token for the user.
        user (UserOutput): The authenticated or registered user's details.
    """
    token: Token
    user: UserOutput


@router.get("/me", response_model=UserOutput, summary="Get current user details")
async def read_users_me(request: Request) -> UserOutput:
    """Retrieve the currently authenticated user's details.

    Returns:
        User: The current authenticated user's details.
    """
    logger.info("Fetching details of the current user.")
    return auth_service.get_current_user(get_header_token(request))


@router.post("/login", response_model=UserData, summary="Login user and retrieve access token")
async def login_for_access_token(
    form_data: UserForLogin,
) -> UserData:
    """Authenticate the user and return an access token if successful.

    Args:
        form_data (UserForLogin): The user's login credentials {email}, {password}.

    Returns:
        UserData: The user's access token and details.

    Raises:
        HTTPException: If authentication fails.
    """
    logger.info("Attempting to log in user with email: %s", form_data.email)
    user_output: UserOutput = auth_service.authenticate_user(
        form_data.email, form_data.password
    )
    if not user_output:
        logger.warning("Authentication failed for email: %s", form_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth_service.create_access_token(
        data={"sub": user_output.email}, expires_delta=access_token_expires
    )
    logger.info("User logged in successfully: %s", user_output.email)
    return UserData(
        token=Token(access_token=access_token, token_type="Bearer"),
        user=user_output
    )


@router.post("/register", response_model=UserData, summary="Register a new user")
async def register_user(
    user: UserForCreate,
) -> UserData:
    """Register a new user and return an access token if successful.

    Args:
        user (UserForCreate): The user's registration details {email}, {password}, {username}.

    Returns:
        UserData: The user's access token and details.

    Raises:
        HTTPException: If the user already exists or another error occurs.
    """
    logger.info("Attempting to register user with email: %s", user.email)
    try:
        user_output: UserOutput = user_service.create_user(user)
    except AlreadyExistsException as e:
        logger.warning(
            "Registration failed, user already exists: %s", user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_output:
        logger.warning(
            "Registration failed: %s", user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth_service.create_access_token(
        data={"sub": user_output.email}, expires_delta=access_token_expires
    )
    logger.info("User registered successfully: %s", user_output.email)
    return UserData(
        token=Token(access_token=access_token, token_type="Bearer"),
        user=user_output
    )
