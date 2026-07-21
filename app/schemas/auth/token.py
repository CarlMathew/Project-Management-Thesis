from datetime import datetime
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email:EmailStr
    password: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class AuthenticationResponse(AccessTokenResponse):
    refresh_expires_at: datetime

class MessageResponse(BaseModel):
    message:str
    
