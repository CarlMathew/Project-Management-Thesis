from datetime import date


from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, session


from app.models import (
    User,
    Priority,
    Project,
    Task,
    TaskStatus,
    TeamMember
    WorkItemType
)


class TaskRepository:
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_task(
        self, 
        task: Task
    ) -> Task:


        self.db.add(task)
        self.db.flush()

        return task

    def get_by_id(
        self,
        task_id: int
    ) -> Task | None:

        statement = (
            select(Task)
            .where(
                Task.task_id == task_id,
                Task.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)

    

    def get_by_code(
        self, 
        task_code: str,
    ) -> Task | None:
    
        statement = (
            select(Task)
            .where(
                Task.task_code == task_code.strip().upper(),
                Task.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)
    

    def user_can_access_project(
        self,
        project: Project,
        user_id: int,
    ) -> bool:

        if project.owner_user_id == user_id:
            return True

        statement = (
            select(TeamMember.user_id)
            .distinct()
            .join(TeamMember, TeamMember.team_id == TeamMember.team_id)
            .where(
                Project.project_id == project.project_id,
                TeamMember.user_id == user_id
            )
        )

        result = self.db.execute(statement).first()

        return result is not None
        

    def list_tasks(
        self,
        *,
        work_item_type_id: int | None,
        project_id: int | None,
        task_status_id: int | None,
        priority_id: int | None,
        reporter_user_id: int | None,
        search_text: str | None,
        offset: int,
        limit: int
    ) -> list[Task]:

        statement = (
            select(Task)
            .where(Task.deleted_at.is_(None))
        )

        return self.db.execute(statement).scalars().all()