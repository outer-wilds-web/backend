from fastapi import HTTPException, Request, status

from api.services import auth_service


def get_header_token(request: Request) -> str:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.split("Bearer ")[1]


def auth_required(request: Request):
    token = get_header_token(request)
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    request.state.user = user
    return user


def allowed_roles(request: Request, allowed_roles: list[str]):
    user = auth_required(request)
    if not any(role in user.roles for role in allowed_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
