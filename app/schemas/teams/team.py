from datetime import datetime

from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    team_name: str = Field(
        min_length=3,
        max_length=100
    )

    description: str| None = Field(
        default=None,
        min_length=1,
        max_length=1000
    )

    department_id: int | None = None
    team_leader_user_id: int | None = None



class TeamUpdate(BaseModel):
    team_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: str| None = Field(
        default=None,
        max_length=1000
    )

    department_id: int | None = None
    team_leader_user_id: int | None = None


class TeamDepartmentResponse(BaseModel):
    department_id: int
    department_name: str


class TeamUserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    full_name: str
    email:str
    job_title:str | None

class TeamResponse(BaseModel):
    team_id: int
    team_name: str
    team_description: str | None
    department: TeamDepartmentResponse | None
    team_lead: TeamUserResponse | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
