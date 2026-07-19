from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.api.dependencies.auth import CurrentUser
from app.db.session import get_db
from app.models import User
from app.schemas import (
    AccessTokenResponse, 
    LoginRequest,
    CurrentUserResponse,
    RoleResponse
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def build_current_user_response(
    user: User,
) -> CurrentUserResponse:
    roles = [
        RoleResponse(
            role_id=user_role.role.role_id,
            role_name=user_role.role.role_name
        )
        for user_role in user.user_roles
        if user_role.role.is_active
    ]

    return CurrentUserResponse(
        user_id=user.user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        job_title=user.job_title,
        profile_image_path=user.profile_image_path,
        is_active=user.is_active,
        roles=roles
    )

@router.post(
    "/login",
    response_model=AccessTokenResponse
)
def login(
    payload: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
) -> AccessTokenResponse: 
    service = AuthService(db)

    user = service.authenticate(
        email=payload.email,
        password=payload.password
    )

    return service.create_token_response(user)


@router.post(
    "/login-form",
    response_model=AccessTokenResponse,
)
def login_form(
    form_data: Annotated[
        OAuth2PasswordRequestForm, 
        Depends()
    ],
    db: Annotated[Session, Depends(get_db)]
) -> AccessTokenResponse:
    service = AuthService(db)

    user = service.authenticate(
        email=form_data.username,
        password=form_data.password
    )

    return service.create_token_response(user)


@router.get(
    "/me",
    response_model = CurrentUserResponse,
)
def get_me(
    current_user: CurrentUser
) -> CurrentUserResponse:
    return build_current_user_response(current_user)
