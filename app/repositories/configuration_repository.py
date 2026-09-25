from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Priority,
    ProjectStatus,
    TaskStatus, 
    WorkItemType
)



class ConfigurationRepository:

    def __init__(self, db: Session):
        self.db = db
    

    def get_active_project_status(
        self
    ) -> list[ProjectStatus]:

        statement = (
            select(ProjectStatus)
            .where(
                ProjectStatus.is_active == True
            )
            .order_by(
                ProjectStatus.display_order,
            )
        )

        return list(self.db.scalars(statement))
    

    def get_active_task_status(
        self
    ) -> list[TaskStatus]:

        statement = (
            select(TaskStatus)
            .where(TaskStatus.is_active == True)
            .order_by(
                TaskStatus.display_order
            )
        )

        return list(self.db.scalars(statement))

    def get_active_priorities(
        self
    ) -> list[Priority]:


        statement = (
            select(Priority)
            .where(Priority.is_active == True)
            .order_by(
                Priority.priority_level
            )
        )

        return list(self.db.scalars(statement))

    def get_active_work_item_types(
        self
    ) -> list[WorkItemType]:

        statement = (
            select(WorkItemType)
            .where(WorkItemType.is_active == True)
            .order_by(
                WorkItemType.display_order
            )
        )

        return list(self.db.scalars(statement))
        

    def get_project_status_id(
        self,
        project_status_id: int
    ) -> ProjectStatus | None:


        statement = (
            select(ProjectStatus)
            .where(
                ProjectStatus.project_status_id == project_status_id,
                ProjectStatus.is_active == True
            )
        )

        return self.db.scalar(statement)


    def get_task_status_id(
        self,
        task_status_id: int
    ) -> TaskStatus | None:

        statement = (
            select(TaskStatus)
            .where(
                TaskStatus.task_status_id == task_status_id,
                TaskStatus.is_active == True
            )
        )

        return self.db.scalar(statement)

    def get_priority_id(
        self,
        priority_id: int
    ) -> Priority | None:
        
        statement = (
            select(Priority)
            .where(
                Priority.priority_id == priority_id,
                Priority.is_active == True
            )
        )


        return self.db.scalar(statement)


    def get_work_item_type_id(
        self,
        work_item_type_id: int
    ) -> WorkItemType | None:

        statement = (
            select(WorkItemType)
            .where(
                WorkItemType.work_item_type_id == work_item_type_id,
                WorkItemType.is_active == True
            )
        )
        return self.db.scalar(statement)

    
