from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext

from api.models.User import User, UserOutput
from api.models.Token import TokenData
from api.repositories import user_repository
from api.services import user_service
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from config.config import get_logger

logger = get_logger()

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the provided password matches the stored hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    logger.debug("Verifying password.")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    logger.debug("Hashing password.")
    return pwd_context.hash(password)


def reset_password(user_id: str, old_password: str, new_password: str) -> bool:
    """Reset a user's password after verifying the old password.

    Args:
        user_id (str): The user's ID.
        old_password (str): The old password to verify.
        new_password (str): The new password to set.

    Returns:
        bool: True if the password was successfully reset, False otherwise.
    """
    logger.info("Attempting to reset password for user ID: %s", user_id)
    user: User = user_repository.get_user_by_id(user_id)

    if not verify_password(old_password, user['hashed_password']):
        logger.warning("Old password does not match for user ID: %s", user_id)
        return False

    user['hashed_password'] = get_password_hash(new_password)
    user_repository.update_user(user_id, user)
    logger.info("Password reset successful for user ID: %s", user_id)
    return True


def create_reset_password_token(email: str) -> str:
    """Create a token for resetting a user's password.

    Args:
        email (str): The user's email.

    Returns:
        str: The reset password token.
    """
    logger.info("Creating reset password token for email: %s", email)
    data = {"sub": email, "exp": datetime.now() + timedelta(minutes=10)}
    logger.debug("Reset password token created for email: %s", email)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_reset_password_token(token: str) -> Union[str, None]:
    """Decode a reset password token to retrieve the email.

    Args:
        token (str): The reset password token.

    Returns:
        Union[str, None]: The email if the token is valid, None otherwise.
    """
    logger.info("Decoding reset password token.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        logger.debug("Reset password token decoded for email: %s", email)
        return email
    except JWTError:
        logger.warning("Failed to decode reset password token.")
        return None


def authenticate_user(email: str, password: str) -> Union[UserOutput, None]:
    """Authenticate a user by verifying their credentials.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        Union[UserOutput, None]: The user's public details if authenticated, None otherwise.
    """
    logger.info("Authenticating user with email: %s", email)
    user: User = user_service.get_user_by_email_with_hashed_password(
        email)
    if not user or not verify_password(password, user.hashed_password):
        logger.warning("Authentication failed for email: %s", email)
        return None
    logger.info("User authenticated successfully: %s", email)
    return UserOutput(
        id=user.id,
        email=user.email,
        username=user.username,
        roles=user.roles
    )


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """Create a JSON Web Token (JWT) for user authentication.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Union[timedelta, None], optional): The token's expiration time. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT.
    """
    logger.info("Creating access token.")
    to_encode = data.copy()
    # print(expires_delta)
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.debug("Access token created.")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOutput:
    """Retrieve the currently authenticated user's details from a token.

    Args:
        token (str): The JWT provided by the user.

    Returns:
        UserOutput: The authenticated user's public details.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    logger.info("Retrieving current user from token.")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except ExpiredSignatureError:
        logger.warning("Token expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        logger.warning("Invalid token.")
        raise credentials_exception

    logger.debug("Token valid, fetching user with email: %s",
                 token_data.email)
    user_output: UserOutput = user_service.get_user_by_email(
        email=token_data.email)
    if user_output is None:
        logger.warning("User not found for email: %s", token_data.email)
        raise credentials_exception
    logger.info("User retrieved successfully: %s", token_data.email)
    return user_output
