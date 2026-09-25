from pydantic import BaseModel, ConfigDict



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


class WorkItemTypResponse(BaseModel):
    work_item_type_id: int

    type_name: str
    type_code: str
    code_prefix: str

    color_hex:str | None
    icon_name: str | None

    display_order:int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )



class ConfigurationResposne(BaseModel):
    project_statuses: list[ProjectStatusResponse]
    task_statuses: list[TaskStatusResponse]
    priorities: list[PriorityResponse]
    work_item_types: list[WorkItemTypResponse]