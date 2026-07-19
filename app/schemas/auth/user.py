from pydantic import BaseModel, ConfigDict, EmailStr


class RoleResponse(BaseModel):
    role_id: int
    role_name: str

    model_config = ConfigDict(from_attributes=True)


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