from datetime import UTC, datetime, time, timedelta
from typing import Any 

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


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



def decode_access_token(token: str) -> dict[str, Any]:
    """
        Decode the token to get user id.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )


        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type") 

        return payload   

    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")


