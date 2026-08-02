from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.config.priority import Priority
from app.api.dependencies.auth import CurrentUser
from app.services.configuration_service import ConfigurationService
from app.schemas import (
    PriorityResponse,
    ProjectStatusResponse,
    TaskStatusResponse
)
from app.services.configuration_service import ConfigurationService


router = APIRouter(
    prefix="/config",
    tags=["Configuration"]
)



@router.get(
    "/project-statuses",
    response_model= list[ProjectStatusResponse]
)
def get_project_statuses(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
) -> list[ProjectStatusResponse]:


    config_service = ConfigurationService(db)

    return [
        ProjectStatusResponse.model_validate(
            project_status
        )
        for project_status 
        in config_service.get_project_statuses()
    ]


@router.get(
    "/task-statuses",
    response_model=list[TaskStatusResponse]
)
def get_task_statuses(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
) -> list[TaskStatusResponse]:
    
    config_service = ConfigurationService(db)

    return [
        TaskStatusResponse.model_validate(
            task_status
        )
        for task_status 
        in config_service.get_task_statuses()
    ]


@router.get(
    "/priorities",
    response_model= list[PriorityResponse]
)
def get_priorities(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
) -> list[Priority]:
    
    config_service = ConfigurationService(db)
    return [
        PriorityResponse.model_validate(
            priority
        )

        for priority in config_service.get_priorities()
    ]
