from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from typing import Any 
from uuid import UUID, uuid4


import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import validates
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def utc_now_naive() -> datetime:
    """
    Return the current UTC time without timezone information

    SQL Server DATETIME2 does not store timezone information, so this 
    application stores all DATETIME2 values as UTC by convention
    """

    return datetime.now(UTC).replace(tzinfo=None)

def hash_password(password: str) -> str:

    """Hash the password so it won't store the original text into database."""
    return password_hash.hash(password)




def verify_password(
    plain_password: str, 
    hashed_password: str) -> bool:
    """
    Check verfiy the hashed password of user
    """
    return password_hash.verify(plain_password, hashed_password)



def create_access_token(subject: str, additional_claims: dict[str, Any] | None=None ) -> str:
    """Create an access token if the user exist on database."""
    
    now = datetime.now(UTC) 
    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expires_at
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def create_refresh_token(
    subject: str,
    token_id: UUID,
    session_family_id: UUID
) -> tuple[str, datetime]:
    now = datetime.now(UTC)
    expires_at = now + timedelta(
        days=settings.refresh_token_expired_days
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "jti": str(token_id),
        "family" :str(session_family_id),
        "iat": now,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    return token, expires_at

def decode_token(
    token: str,
    expected_type: str,
) -> dict[str, Any]:
    payload = jwt.decode(
        token, 
        settings.jwt_secret_key, 
        algorithms=[settings.jwt_algorithm]
    )

    if payload.get("type") != expected_type:
        raise InvalidTokenError(
            f"Expected a {expected_type} token"
        ) 


    if not payload.get("sub"):
        raise InvalidTokenError("Token subject is missing")
    
    if not payload.get("jti"):
        raise InvalidTokenError("Token Identifier is missing")

    return payload


def decode_access_token(token: str) -> dict[str, Any]:

    return decode_token(
        token=token,
        expected_type="access "
    )


def decode_refresh_token(token: str) -> dict[str, Any]:
    return decode_token(
        token=token,
        expected_type="refresh"
    )


