from __future__ import annotations

from pydantic import (
    BaseModel, 
    ConfigDict, 
    EmailStr, 
    Field
)

class CurrentUserResponse(BaseModel):
    user_id: int
    email: EmailStr
    first_name:str
    last_name:str
    full_name: str
    job_title: str | None
    profile_image_path: str | None
    is_active: bool
    roles: list[RoleResponse]



class RoleResponse(BaseModel):
    role_id: int
    role_name: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr

    first_name: str = Field(
        min_length=1,
        max_length=100
    )

    last_name: str = Field(
        min_length=1,
        max_length=100
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )

    job_title: str | None = Field(
        default=None,
        max_length=150
    )

    department_id: int | None = None

    role_ids: list[int] = Field(
        default_factory=list
    )

class UserUpdate(BaseModel):
    first_name: str | None = Field(
        default = None,
        min_length=1,
        max_length=100
    )

    last_name: str | None = Field(
        default = None,
        min_length=1,
        max_length=100
    )

    job_title: str | None = Field(
        default = None,
        min_length=1,
        max_length=500
    )

    role_ids: list[int] | None = Field(
        default_factory=list
    )

    department_id: int | None = None

    
