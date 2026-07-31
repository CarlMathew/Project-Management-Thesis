from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import (
    Priority,
    ProjectStatus,
    TaskStatus
)
from app.repositories.configuration_repository import ConfigurationRepository



class ConfigurationService:

    def __init__(self, db: Session):
        self.configuration_repository = ConfigurationRepository(db)

    def get_project_statuses(self) -> list[ProjectStatus]:
        return self.configuration_repository.get_active_project_status()
    
    def get_task_statuses(self) -> list[TaskStatus]:
        return self.configuration_repository.get_active_task_status()

    def get_priorities(self) -> list[Priority]:
        return self.configuration_repository.get_active_priorities()

    
    def get_project_status(
        self,
        project_status_id: int
    ) -> ProjectStatus:


        project_status = (
            self.configuration_repository
            .get_project_status_id(
                project_status_id
            )
        )

        if project_status is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"The selected project status doesn't exist or inactive"
            )
        
        return project_status
    
    def get_task_status(
        self,
        task_status_id: int
    ) -> TaskStatus:

        task_status = (
            self.configuration_repository
            .get_task_status_id(task_status_id)
        )

        if task_status is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f" The selected task status doesn't exist or inactive"
            )

        return task_status
    

    def get_priority(
        self, 
        priority_id: int
    ) -> Priority:

        priority = (
            self.configuration_repository
            .get_priority_id(priority_id)
        )

        if priority is None:

            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f" The selected priority doesn't exist or inactive"
            )

        return priority
    

    
