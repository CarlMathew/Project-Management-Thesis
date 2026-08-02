from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.core import department


class DepartmentCreate(BaseModel):
    department_name: str = Field(
        min_length=1,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    manager_user_id: int | None = None
    supervisor_user_id: int | None = None


    @model_validator(mode="after")
    def validate_leadership_assignments(
        self,
    ) -> "DepartmentCreate":

        if (
            self.manager_user_id and 
            self.manager_user_id == self.supervisor_user_id
        ):
            raise ValueError(
                "The manager and supervisor must be different users"
            )

        return self

class DepartmentUpdate(BaseModel):
    department_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    manager_user_id: int | None = None
    supervisor_user_id: int | None = None

    @model_validator(mode="after")
    def validate_leadership_assignments(
        self,
    ) -> "DepartmentUpdate":

        provided_details = self.model_fields_set

        manager_was_provided = "manager_user_id" in provided_details
        supervisor_was_provided = "supervisor_user_id" in provided_details

        if (
            manager_was_provided and 
            supervisor_was_provided and
            self.manager_user_id == self.supervisor_user_id
        ):
            raise ValueError(
                "The manager and supervisor must be different users"
            )

        return self



class DepartmentUserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    job_title: str | None


    model_config = ConfigDict(
        from_attributes=True
    )

class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    description: str
    manager:  DepartmentUserResponse | None
    supervisor: DepartmentUserResponse | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class MessageResponse:
    message: str
