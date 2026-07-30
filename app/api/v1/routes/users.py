from typing import Annotated

from fastapi import (
    APIRouter, 
    Depends, 
    Query, 
    Request,
    status
)
from sqlalchemy.orm import Session

from app.api.v1.routes.auth import build_current_user_response
from app.api.dependencies.auth import require_permission
from app.db.session import get_db
from app.models import User
from app.core.limiter import limiter
from app.schemas import (
    UserCreate,
    CurrentUserResponse,
    UserUpdate
)

from app.services.user_service import UserService



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


UserViewer = Annotated[User, Depends(require_permission("user.view"))]
UserManager = Annotated[User, Depends(require_permission("user.manage"))]


@router.post(
    "",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("30/minute")
def create_user(
    payload: UserCreate,
    request: Request,
    current_user: UserManager,
    db: Annotated[Session, Depends(get_db)]
) -> CurrentUserResponse:
    service = UserService(db)


    user = service.create_user(
        payload=payload,
        created_by = current_user.user_id
    )

    return build_current_user_response(user)


@router.get(
    "",
    response_model=list[CurrentUserResponse],
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def list_users(
    current_user: UserViewer,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50
) -> list[CurrentUserResponse]:


    service = UserService(db)


    users = service.list_users(
        offset=offset,
        limit=limit
    )

    return [
        build_current_user_response(user)
        for user in users
    ]

@router.get(
    "/{user_id}",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def get_user(
    user_id: int,
    request: Request,
    current_user: UserViewer,
    db: Annotated[Session, Depends(get_db)]
) -> CurrentUserResponse:


    service = UserService(db)
    user = service.get_user(user_id)

    return build_current_user_response(user)


@router.patch(
    "/{user_id}",
    response_model=CurrentUserResponse
)
@limiter.limit("30/minute")
def update_user(
    user_id: int,
    request: Request,
    payload: UserUpdate,
    current_user: UserManager,
    db: Annotated[Session, Depends(get_db)]
) -> CurrentUserResponse:

    service = UserService(db)
    user = service.update_user(
        user_id=user_id,
        payload=payload,
        updated_by=current_user.user_id
    )
    return build_current_user_response(user)


@router.post(
    "/{user_id}/deactivate",
    response_model=CurrentUserResponse
)
@limiter.limit("30/minute")
def deactivate_user(
    user_id: int,
    request: Request,
    current_user: UserManager,
    db: Annotated[Session, Depends(get_db)]
) -> CurrentUserResponse:

    service = UserService(db)
    user = service.deactivate_user (
        user_id=user_id,
        deactivated_by=current_user.user_id
    )

    return build_current_user_response(user)


@router.post(
    "/{user_id}/activate",
    response_model=CurrentUserResponse
)
@limiter.limit("30/minute")
def activate_user(
    user_id: int,
    request: Request,
    current_user: UserManager,
    db: Annotated[Session, Depends(get_db)]
) -> CurrentUserResponse:

    service = UserService(db)

    user = service.activate_user(
        user_id=user_id,
        activated_by=current_user.user_id
    )

    return build_current_user_response(user)