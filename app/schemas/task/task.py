from datetime import date, datetime
from decimal import Decimal


from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator
)

from app.schemas.configuration.configuration import (
    TaskStatusResponse,
    PriorityResponse,
    WorkItemTypResponse, 
)

from app.schemas.projects.projects import (
    ProjectResponse
)


class TaskCreate(BaseModel):

    work_item_type_id: int

    project_id: int | None = None
    parent_task_id: int | None = None


    title: str = Field(
        min_length=1,
        max_length=300
    )

    description: str | None = None

    task_status_id: int
    priority_id: int

    reporter_user_id: int | None = None

    start_date: date | None
    due_date: date | None

    estimated_hours: Decimal | None = Field(
        default = None,
        ge = 0,
        max_digits=10,
        decimal_places=2
    )

    actual_hours: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2
    )

    display_order: Decimal | None = Field(
        default=None,
        max_digits=18,
        decimal_places=6
    )

    @field_validator("description")
    @classmethod
    def clean_description(
        cls,
        value: str | None
    ) -> str | None:
        
        if value is None:
            return None
        
        return value.strip() or None


    
    @model_validator(mode="after")
    def validate_dates(self) -> "TaskCreate":
        if(
            self.start_date is not None
            and self.due_date is not None
            and self.due_date < self.start_date
        ):

            raise ValueError(
                "Due date cannot be before start date"
            )

        return self


class TaskUpdate(BaseModel):
    project_id: int | None = None
    parent_task_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: str | None = None

    task_status_id: int | None = None
    priority_id: int | None = None

    reporter_user_id: int | None = None

    start_date: date | None
    due_date: date | None

    estimated_hours: Decimal | None = Field(
        default = None,
        ge = 0,
        max_digits=10,
        decimal_places=2
    )

    actual_hours: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2
    )

    display_order: Decimal | None = Field(
        default=None,
        max_digits=18,
        decimal_places=6
    )

    @field_validator("title")
    @classmethod
    def clean_title(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return None
        
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Title cannot be empty"
            )

        return cleaned_value
    

    @field_validator("description")
    @classmethod
    def clean_description(
        cls,
        value: str | None
    ) -> str | None:
        
        if value is None:
            return None
        
        return value.strip() or None


    
    @model_validator(mode="after")
    def validate_dates(self) -> "TaskUpdate":
        if(
            self.start_date is not None
            and self.due_date is not None
            and self.due_date < self.start_date
        ):

            raise ValueError(
                "Due date cannot be before start date"
            )

        return self





class ParentTaskSummary(BaseModel):
    project_id: int
    project_code: str
    project_name: str

class TaskUserSummary:
    user_id: int
    full_name: str
    email: str
    job_title: str | None


class TaskResponse(BaseModel):

    task_id: str
    task_code: str

    work_item_type: WorkItemTypResponse
    project: ProjectResponse | None
    parent_task: ParentTaskSummary | None

    title: str
    description: str | None

    status: TaskStatusResponse
    priority: PriorityResponse
    reporter: TaskUserSummary 

    start_date: date | None
    due_date: date | None

    estimated_hours: Decimal | None
    actual_hours: Decimal | None

    completed_at: datetime | None
    display_order: Decimal | None
    
    created_at: datetime
    updated_at: datetime
