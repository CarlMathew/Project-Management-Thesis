from _typeshed import StrPath
from re import I

from pydantic import BaseModel, ConfigDict

from app.models.config import project_status


class ProjectStatusResponse(BaseModel):
    project_status_id: int
    status_name: str
    status_code: str
    color_hex: str
    display_order: int
    is_closed_status: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class TaskStatusResponse(BaseModel):
    task_status_id: int
    status_name: str
    status_code: str
    color_hex: str
    display_order: int
    is_completed_status: bool
    is_cancelled_status: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class PriorityResponse(BaseModel):
    priority_id: int
    priority_name: str
    priority_code: str
    priority_level: int
    color_hex: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )



class ConfigurationResposne(BaseModel):
    project_statuses: list[ProjectStatusResponse]
    task_statuses: list[TaskStatusResponse]
    priorities: list[PriorityResponse]