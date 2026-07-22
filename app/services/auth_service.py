from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_token, 
    utc_now_naive,
    verify_password,
)
from app.models import User, RefreshSession
from app.repositories.refresh_session_repository import RefreshSessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas import (
    AccessTokenResponse,  
    AuthenticationResponse
)

INVALID_CREDENTIALS_MESSAGE = "Incorrect email or password"
INVALID_REFRESH_TOKEN_MESSAGE = "Invalid token or expired refresh token"



@dataclass
class IssuedTokens:
    response: AuthenticationResponse
    refresh_token: str

class AuthService:
    def __init__(self, db:Session) -> None:
        self.user_repository = UserRepository(db)

    def authenticate(
        self,
        email:str,
        password: str
    ) -> User:
        """Autheticate the user if exist."""

        normalized_email = email.strip().lower()

        user = self.user_repository.get_by_email(normalized_email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS_MESSAGE,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code =  status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS_MESSAGE,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = "This account is inactive"
            )

        
        self.user_repository.update_last_login(user)

        return user

    # # TODO: Finalize the set last login
    # def login(
    #     self,
    #     *,
    #     email: str,
    #     password: str, 
    #     ip_address: str | None,
    #     user_agent: str | None
    # ) -> IssuedTokens:
    #     user = self.authenticate(email, password)

    #     issued_tokens = self._create_new_session(
    #         user=user,
    #         ip_address=ip_address,
    #         user_agent=user_agent
    #     )

    #     self.user_repository.set_last_login(
    #         user=user,
    #         last_login_at=utc_now_naive()
    #     )

    #     self.db.commit()

    #     return issued_tokens
    
    def create_token_response(
        self,
        user: User
    ) -> AccessTokenResponse:

        role_names = [
            user_role.role.role_name
            for user_role in user.user_roles
            if user_role.role.is_active
        ]


        access_token = create_access_token(
            subject=str(user.user_id),
            additional_claims={
                "roles": role_names
            }
        )

        return AccessTokenResponse(
            access_token=access_token,
            expires_in=settings.access_token_expire_minutes * 60
        )