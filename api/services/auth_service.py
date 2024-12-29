from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError

from api.models.User import User, UserOutput
from api.models.Token import TokenData

from api.repositories import user_repository
from api.services import user_service

SECRET_KEY = "5e1fc44a970f7c27d0b1ad5956053840c628cc2c731e3eb5ea67df02ddf6af28"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def reset_password(userId, old_password, new_password):
    user: User = user_repository.get_user_by_id(userId)

    if not verify_password(old_password, user['hashed_password']):
        return False

    user['hashed_password'] = get_password_hash(new_password)
    user_repository.update_user(userId, user)
    return True


def create_reset_password_token(email: str):
    data = {"sub": email, "exp": datetime.now() + timedelta(minutes=10)}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except JWTError:
        print(payload)
        return None


def authenticate_user(email: str, password: str) -> UserOutput:
    user: User = user_service.get_user_by_email_with_hashed_password(
        email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    user_output: UserOutput = UserOutput(
        id=user.id,
        email=user.email,
        username=user.username,
        roles=user.roles
    )
    return user_output


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    # print(expires_delta)
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserOutput:
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
        # print(payload)
        token_data = TokenData(email=email)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception

    user_output: UserOutput = user_service.get_user_by_email(
        email=token_data.email)
    if user_output is None:
        raise credentials_exception
    return user_output
