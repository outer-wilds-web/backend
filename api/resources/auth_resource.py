from datetime import timedelta
from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import BaseModel

from config.config import config
from api.dependancies import get_header_token
from api.exceptions import AlreadyExistsException
from api.models.Token import Token
from api.models.User import User, UserForCreate, UserForLogin, UserOutput
from api.repositories import user_repository
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
    return UserData(token=Token(access_token=access_token, token_type="bearer"), user=user_output)


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
    return UserData(token=Token(access_token=access_token, token_type="bearer"), user=user_output)


# class ForgetPassword(BaseModel):
#     email: str


# @router.post("/forget-password")
# async def forget_password(
#     background_tasks: BackgroundTasks,
#     email: ForgetPassword
# ):
#     email = email.email
#     try:
#         user_output: UserOutput = user_service.find_user_by_email(email)
#         if user_output is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Email non trouvé",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         secret_token = auth_service.create_reset_password_token(email)
#         forget_url_link = f"""{config["frontend"]
#                                ["url"]}/reset-password/{secret_token}"""

#         html = f"""<html>
#             <body>
#                 <h1>Réinitialisation de mot de passe</h1>
#                 <p>Bonjour, <br>
#                 Vous avez demandé une réinitialisation de mot de passe pour votre compte.
#                 Veuillez cliquer sur
#                 <a href="{forget_url_link}">ce lien</a> pour réinitialiser votre mot de passe.
                
#             </body>
#         </html>"""

#         message = MessageSchema(
#             subject="Réinitialisation de mot de passe",
#             recipients=[email],
#             body=html,
#             subtype=MessageType.html
#         )

#         fm = FastMail(fm_config)
#         background_tasks.add_task(fm.send_message, message)

#         return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Email envoyé", "success": True, "status_code": status.HTTP_200_OK})

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# class ResetPassword(BaseModel):
#     token: str
#     password: str


# @router.post("/reset-password")
# async def reset_password(
#     reset_password: ResetPassword,
# ):
#     email = auth_service.decode_reset_password_token(reset_password.token)
#     if email is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token invalide",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user: User = user_repository.find_user_by_email(email)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Email non trouvé",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user["hashed_password"] = auth_service.get_password_hash(
#         reset_password.password)
#     print(user)
#     user_repository.update_user(user['_id'], user)
#     return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Mot de passe réinitialisé", "success": True, "status_code": status.HTTP_200_OK})
