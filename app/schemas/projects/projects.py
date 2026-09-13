from datetime import datetime
from pydantic import BaseModel,  Field


class ProjectCreate(BaseModel):

    project_name: str = Field(
        min_length=5,
        max_length=100
    )

    description: str | None = Field(
        min_length=1,
        max_length=1000,
        default=None
    )

    team_id: int | None = Field(
        default=None
    )

    project_status_id: int = Field(
        default=1
    )

    priority_id: int

    start_date: datetime | None = None

    target_end_date: datetime | None = None



class ProjectUpdate(BaseModel):

    project_name: str | None = Field(
        default=None,
        min_length=5,
        max_length=100

    )

    description: str | None = Field(
        min_length=1,
        max_length=1000,
        default=None
    )

    team_id: int | None = Field(
        default=None 
    )

    project_status_id: int | None = Field(
        default=None
    )

    priority_id: int | None = Field(
        default=None
    )

    start_date: datetime | None = None

    target_end_date: datetime | None = None


class ProjectOwnerResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    job_title: str | None

class ProjectTeamResponse(BaseModel):
    team_name: str
    description: str
    team_lead_user_id: int

class ProjectResponse(BaseModel):
    project_id:int
    project_code: str
    project_name: str
    description: str | None
    project_status_id: int
    team: ProjectTeamResponse | None
    priority_id: int
    owner: ProjectOwnerResponse
    start_date: datetime | None
    target_end_date:  datetime | None
