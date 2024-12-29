from uuid import UUID

from api.exceptions import AlreadyExistsException
from api.models.User import User, UserForCreate, UserForUpdate, UserOutput
from api.repositories import user_repository
from api.services import auth_service


def create_user(user: UserForCreate) -> UserOutput:
    if get_user_by_email(user.email):
        raise AlreadyExistsException("User already exists")

    user: User = User(
        email=user.email,
        username=user.username,
        hashed_password=auth_service.get_password_hash(user.password)
    )
    user_repository.create_user(user.model_dump(by_alias=True))

    # Get the user with the id
    user_output: UserOutput = get_user_by_id(user.id)

    return user_output


def get_users() -> list[UserOutput]:
    users = user_repository.get_users()

    users = [{
        'id': UUID(user[0]),
        'email': user[1],
        'username': user[2],
        'roles': user[4]
    } for user in users]

    return [UserOutput(
        id=user['id'],
        email=user['email'],
        username=user['username'],
        roles=user['roles']
    ) for user in users]


def get_user_by_email(email: str) -> UserOutput:
    result = user_repository.get_user_by_email(email)

    if not result:
        return None

    result = {
        'id': UUID(result[0]),
        'email': result[1],
        'username': result[2],
        'hashed_password': result[3],
        'roles': result[4]
    }

    user_output: UserOutput = UserOutput(
        id=result['id'],
        email=result['email'],
        username=result['username'],
        roles=result['roles']
    )
    return user_output


def get_user_by_email_with_hashed_password(email: str) -> User:
    result = user_repository.get_user_by_email(email)
    if not result:
        return None

    result = {
        'id': UUID(result[0]),
        'email': result[1],
        'username': result[2],
        'hashed_password': result[3],
        'roles': result[4]
    }

    user = User(
        email=result['email'],
        username=result['username'],
        roles=result['roles'],
        hashed_password=result['hashed_password']
    )
    # Update the user id after the object creation because Python
    user.id = result['id']
    return user


def get_user_by_id(user_id: UUID) -> UserOutput:
    result = user_repository.get_user_by_id(user_id)
    if not result:
        return None

    result = {
        'id': UUID(result[0]),
        'email': result[1],
        'username': result[2],
        'hashed_password': result[3],
        'roles': result[4]
    }

    user_output: UserOutput = UserOutput(
        id=result['id'],
        email=result['email'],
        username=result['username'],
        roles=result['roles']
    )
    return user_output


def update_user(user_id: UUID, user: UserForUpdate) -> UserOutput:
    other_user = get_user_by_email(user.email)
    if other_user and other_user.id != user_id:
        raise AlreadyExistsException("User already exists")

    modify_count = user_repository.update_user(
        user_id, user.model_dump(by_alias=True))

    return get_user_by_id(user_id)


def grant_admin(user_id: UUID) -> UserOutput:
    user = get_user_by_id(user_id)
    if not user:
        return None

    user.roles.append("admin")
    modify_count = user_repository.update_user(
        user_id, user.model_dump(by_alias=True))
    print("Droit accordé a l'administrateur")
    return get_user_by_id(user_id)


def delete_user(user_id: UUID) -> int:
    return user_repository.delete_user(user_id)
