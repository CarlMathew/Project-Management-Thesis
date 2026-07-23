from dataclasses import dataclass
from datetime import UTC

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
        self.db = db
        self.user_repository = UserRepository(db)
        self.refresh_repository = RefreshSessionRepository(db)

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


        return user

    # TODO: Finalize the set last login
    def login(
        self,
        *,
        email: str,
        password: str, 
        ip_address: str | None,
        user_agent: str | None
    ) -> IssuedTokens:

        user = self.authenticate(email, password)

        issued_tokens = self._create_new_session(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent
        )

        self.user_repository.set_last_login(
            user=user,
            last_login_at=utc_now_naive()
        )

        self.db.commit()

        return issued_tokens
    
    def refresh(
        self,
        *,
        refresh_token: str,
        ip_address: str | None,
        user_agent: str | None
    ) -> IssuedTokens:
        try:
            payload = decode_refresh_token(refresh_token)
            
            user_id = int(payload["sub"])
            token_id = UUID(payload["jti"])
            family_id = UUID(payload["family"])

        except(
            InvalidTokenError,
            KeyError,
            TypeError,
            ValueError
        ) as exc:
            raise self._invalid_refresh_token_exception() from exc
        

        stored_token_hash = hash_token(refresh_token)

        refresh_session = (
            self.refresh_repository.get_by_token_hash(
                stored_token_hash
            )
        )

        if refresh_session is None:
            raise self._invalid_refresh_token_exception()
        

        if (
            refresh_session.token_id != token_id
            or refresh_session.session_family_id != family_id
            or refresh_session.user_id != user_id
        ):
            raise self._invalid_refresh_token_exception()
        
        now = utc_now_naive()

        if refresh_session.revoked_at is not None:
            self.refresh_repository.revoke_family(
                session_family_id=family_id,
                revoked_at=now
            )

            self.db.commit()


            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail=(
                    """
                    Refresh token reuse was detected
                    Please sign in again.
                    """
                ),
                headers={"WWW-Authenticate": "Bearer"}
            )
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise self._invalid_refresh_token_exception()
        
        if not user.is_active:
            self.refresh_repository.revoke_family(
                session_family_id=family_id,
                revoked_at=now
            )
            self.db.commit()


            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="The account is inactive"
            )


        new_token_id = uuid4()

        new_refresh_token, refresh_token_expires_at_aware = (
            create_refresh_token(
                subject=str(user.user_id),
                token_id = new_token_id, 
                session_family_id=family_id
            )
        )

        refresh_expires_at = (
            refresh_token_expires_at_aware.astimezone(UTC)
            .replace(tzinfo=None)
        )


        refresh_session.revoked_at = now
        refresh_session.last_used_at = now
        refresh_session.replaced_by_token_id = new_token_id

        self.db.add(refresh_session)


        self.refresh_repository.create(
            user_id= user.user_id,
            session_family_id=family_id,
            token_id=new_token_id,
            token_hash=hash_token(new_refresh_token),
            expires_at = refresh_expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )

        access_token = self._create_access_token(user)

        self.db.commit()

        return IssuedTokens(
            response=AuthenticationResponse(
                access_token=access_token,
                expires_in=(
                    settings.access_token_expire_minutes * 60
                ),
                refresh_expires_at=refresh_expires_at
            ),
            refresh_token=new_refresh_token
        )

        

    def _create_new_session(
        self, 
        *,
        user: User,
        ip_address: str | None,
        user_agent: str | None
    ) -> IssuedTokens:
        session_family_id = uuid4()
        token_id = uuid4()

        refresh_token, refresh_expires_at_aware = (
            create_refresh_token(
                subject=str(user.user_id),
                token_id=token_id,
                session_family_id=session_family_id
            )
        )


        refresh_expires_at = (
            refresh_expires_at_aware.astimezone(UTC)
            .replace(tzinfo=None)
        )


        self.refresh_repository.create(
            user_id= user.user_id,
            session_family_id=session_family_id,
            token_id=token_id,
            token_hash=hash_token(refresh_token),
            expires_at = refresh_expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )

        access_token = self._create_access_token(user)

        
        return IssuedTokens(
            response=AuthenticationResponse(
                access_token=access_token,
                expires_in=(
                    settings.access_token_expire_minutes * 60
                ),
                refresh_expires_at=refresh_expires_at
            ),
            refresh_token=refresh_token
        )

    def logout(
        self,
        refresh_token: str | None
    ) -> None:
        if not refresh_token:
            return
        
        refresh_session = (
            self.refresh_repository.get_by_token_hash(
                hash_token(refresh_token)
            )
        )

        if (
            refresh_session is not None
            and refresh_session.revoked_at is None
        ):
            self.refresh_repository.revoke_session(
                refresh_session,
                revoked_at=utc_now_naive()
            )

            self.db.commit()

    
    def logout_all(
        self,
        user_id: int
    ) -> None:
        self.refresh_repository.revoke_all_for_users(
            user_id = user_id,
            revoked_at=utc_now_naive()
        )
        self.db.commit()


    def revoke_session(
        self,
        *,
        refresh_session_id: int,
        user_id: int
    ) -> None:
        refresh_session = (
            self.refresh_repository.get_active_session_by_id(
                refresh_session_id=refresh_session_id,
                user_id = user_id
            )
        )

        if refresh_session is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Active session not found"
            )
        

        self.refresh_repository.revoke_session(
            refresh_session,
            revoked_at=utc_now_naive()
        )


        self.db.commit()

    def get_active_session(
        self,
        user_id: int,
        refresh_session_id:int
    ) -> RefreshSession | None:
        return self.refresh_repository.get_active_session_by_id(
            refresh_session_id=refresh_session_id,
            user_id= user_id
        )

    
    def _create_access_token(
        self,
        user: User,
    ) -> str:
        role_names = [
            user_role.role.role_name
            for user_role in user.user_roles
            if user_role.role.is_active
        ]

        return create_access_token(
            subject=str(user.user_id),
            additional_claims={
                "roles": role_names
            }
        )
    
    @staticmethod
    def _invalid_credentials_exception() -> HTTPException:
        return HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @staticmethod
    def _invalid_refresh_token_exception() -> HTTPException:
        return HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_REFRESH_TOKEN_MESSAGE,
            headers= {"WWW-Authenticate":"Bearer"}
        )

