from typing import Annotated

from app import services
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.routes.auth import build_current_user_response
from app.api.dependencies.auth import require_permission
from app.db.session import get_db
from app.models import User
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
def create_user(
    payload: UserCreate,
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
    response_model=list[CurrentUserResponse]
)
def list_users(
    current_user: UserViewer,
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