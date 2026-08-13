from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict



class AddMember(BaseModel):
    team_id: int
    user_id: int

    member_role: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    capacity_percentage: Decimal = Field(
        default= Decimal("100.00"),
        ge=0,
        le=100
    )

class UpdateMember(BaseModel):
    member_role: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    capacity_percentage: Decimal | None = Field(
        default= None,
        ge=0.00,
        le=100.00
    )

class TeamMemberTeamResponse(BaseModel):
    team_id: int
    team_name: str
    team_description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamMemberUserResponse(BaseModel):
    team_member_id: int
    user_id: int
    full_name: str
    email:str
    job_title:str | None
    member_role: str
    capacity_percentage: float

    model_config = ConfigDict(from_attributes=True)



