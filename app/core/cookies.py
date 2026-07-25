from fastapi import Response

from app.core.config import settings



def set_refresh_token_cookie(
    response: Response,
    refresh_token: str
) -> None:
    max_age = settings.refresh_token_expired_days * 24 * 60 * 60

    response.set_cookie(
        key=settings.refresh_token_cookie_name,
        value=refresh_token,
        max_age=max_age,
        path=settings.refresh_token_cookie_path,
        secure=settings.refresh_token_cookie_secure,
        httponly=True,
        samesite=settings.refresh_token_cookie_samesite
    )

def delete_refresh_token_cookie(
    response: Response,
) -> None:

    response.delete_cookie(
        key=settings.refresh_token_cookie_name,
        path=settings.refresh_token_cookie_path,
        secure=settings.refresh_token_cookie_secure,
        httponly=True,
        samesite=settings.refresh_token_cookie_samesite
    )

