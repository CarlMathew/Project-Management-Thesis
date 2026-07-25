from collections.abc import Callable
from typing import Annotated


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session


from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login-form"
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception
        

        user_id = int(subject)

    except (InvalidTokenError, TypeError, ValueError) as exc:
        raise credentials_exception from exc
    

    repository = UserRepository(db)
    user = repository.get_by_id(user_id)

    if user is None: 
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive"
        )
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_user_permission_codes(
    user: User,
) -> set:

    return {
        role_permission.permission.permission_code
        for user_role in user.user_roles
        if user_role.role.is_active
        for role_permission in user_role.role.role_permissions
    }


def require_permission(
    permission_code: str
) -> Callable[[CurrentUser], User]:

    def permission_dependency(
        current_user: CurrentUser
    ) -> User:

        permission_codes = get_user_permission_codes(
            current_user
        )


        if permission_code not in permission_codes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail =(
                    f"Permission required: {permission_code}"
                )
            )

        return current_user
    return permission_dependency