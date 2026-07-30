from typing import Annotated
from fastapi import (
    APIRouter, 
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status

)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.api.dependencies.auth import CurrentUser
from app.core.config import settings
from app.core.limiter import limiter
from app.core.security import hash_token


from app.core.cookies import (
    set_refresh_token_cookie,
    delete_refresh_token_cookie
)
from app.db.session import get_db
from app.models import User
from app.schemas import (
    AuthenticationResponse,
    CurrentUserResponse, 
    LoginRequest,
    MessageResponse,
    RefreshSessionResponse,
    RoleResponse,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_client_ip(request: Request) -> str | None:

    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    if request.client:
        return request.client.host

    return None

def get_user_agent(request: Request) -> str | None:
    user_agent = request.headers.get("user-agent")

    if user_agent is None:
        return None
        
    return user_agent[:1000]


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
    response_model=AuthenticationResponse
)
@limiter.limit("5/minute")
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)]
) -> AuthenticationResponse: 
    service = AuthService(db)

    issued_tokens = service.login(
        email=str(payload.email),
        password = payload.password,
        ip_address = get_client_ip(request),
        user_agent=get_user_agent(request)
    )


    set_refresh_token_cookie(
        response,
        issued_tokens.refresh_token

    )
    return issued_tokens.response

@router.post(
    "/login-form",
    response_model=AuthenticationResponse
)
@limiter.limit("5/minute")
def login_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)]
) -> AuthenticationResponse: 
    service = AuthService(db)

    issued_tokens = service.login(
        email=str(form_data.username),
        password = form_data.password,
        ip_address = get_client_ip(request),
        user_agent=get_user_agent(request)
    )


    set_refresh_token_cookie(
        response,
        issued_tokens.refresh_token

    )
    return issued_tokens.response

@router.post(
    "/refresh",
    response_model=AuthenticationResponse
)
@limiter.limit("20/minute")
def refresh_access_token(
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    refresh_token: Annotated[
        str | None,
        Cookie(alias=settings.refresh_token_cookie_name)
    ]
) -> AuthenticationResponse:

    if refresh_token is None:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cookie is missing"
        )


    service = AuthService(db)

    issued_tokens = service.refresh(
        refresh_token=refresh_token,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )


    set_refresh_token_cookie(
        response,
        issued_tokens.refresh_token
    )

    return issued_tokens.response


@router.post(
    "/logout",
    response_model=MessageResponse
)
@limiter.limit("20/minute")
def logout(
    response: Response,
    request:Request,
    db: Annotated[Session, Depends(get_db)],
    refresh_token: Annotated[
        str | None,
        Cookie(alias=settings.refresh_token_cookie_name),
    ] = None
    
) -> MessageResponse:
    service = AuthService(db)
    service.logout(refresh_token)

    delete_refresh_token_cookie(response)

    return MessageResponse(
        message= "Logout successful"
    )

@router.post(
    "/logout-all",
    response_model=MessageResponse
)
@limiter.limit("20/minute")
def logout_all(
    current_user: CurrentUser,
    response: Response,
    request:Request,
    db: Annotated[Session, Depends(get_db)]
) -> MessageResponse:
    service = AuthService(db)
    service.logout_all(current_user.user_id)

    delete_refresh_token_cookie(response)

    return MessageResponse(
        message="All sessions have been logged out."
    )


@router.get(
    "/sessions",
    response_model = list[RefreshSessionResponse]
)
@limiter.limit("30/minute")
def get_sessions(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    request:Request,
    refresh_token: Annotated[
        str | None,
        Cookie(alias=settings.refresh_token_cookie_name)
    ] = None    
) -> list[RefreshSessionResponse]:
  

    service = AuthService(db)

    sessions = service.get_active_sessions(current_user.user_id)

    current_token_hash = (
        hash_token(refresh_token)
        if refresh_token
        else None
    )

    return [
        RefreshSessionResponse(
            refresh_session_id=session.refresh_session_id,
            created_at = session.created_at,
            last_used_at = session.last_used_at,
            expires_at=session.expires_at,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            is_current = (
                current_token_hash is not None
                and session.token_hash == current_token_hash
            )
        )
        for session in sessions
    ]

@router.delete(
    "/sessions/{refresh_session_id}",
    response_model = MessageResponse
)
@limiter.limit("30/minute")
def revoke_session(
    refresh_session_id: int,
    request:Request,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
) -> MessageResponse:

    service = AuthService(db)

    service.revoke_session(
        refresh_session_id=refresh_session_id,
        user_id=current_user.user_id
    )

    return MessageResponse(
        message="Session revoked successfully"
    )




@router.get(
    "/me",
    response_model = CurrentUserResponse,
)
@limiter.limit("60/minute")
def get_me(
    current_user: CurrentUser,
    request: Request
) -> CurrentUserResponse:
    return build_current_user_response(current_user)
