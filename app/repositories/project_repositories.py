from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models import (
    Project,
    User,
    Team
)


class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        project: Project
    ) -> Project:

        self.db.add(project)
        self.db.flush()

        return project

    def get_by_id(
        self,
        project_id: int
    ) -> Project | None:

        statement = (
            select(Project)
            .where(
                Project.project_id== project_id,
                Project.deleted_at.is_(None)
            )
        ) 

        return self.db.scalar(statement)
    

    def get_by_project_name( 
        self, 
        project_name: str
    ) -> Project | None:

        statement = (
            select(Project)
            .where(
                Project.project_name == project_name,
                Project.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)

    
    def get_by_project_code(
        self,
        project_code: str
    ) -> Project | None :        
        statement = (
            select(Project)
            .where(
                Project.project_code == project_code,
                Project.deleted_at.is_(None)
            )
        ) 

        return self.db.scalar(statement)

    def get_owner(
        self,
        project_id: int | None
    ) -> User:

        statement = (
            select(Project)
            .where(Project.project_id == project_id)
        )

        project = self.db.scalar(statement)

        return project.owner 
    
    def get_team(
        self,
        project_id: int | None
    ) -> Team | None:
        statement = (
            select(Project)
            .where(Project.project_id == project_id)
        )

        project = self.db.scalar(statement)

        if project is None:
            return None

        return project.team
        
    
    def list_projects(
        self,
        project_name: str | None,
        project_status_id: int | None,
        priority_id: int | None,
        owner_user_id: int | None,
        team_id: int | None,
        is_active: bool,
        offset: int,
        limit: int 
    ) -> list[Project]:

        statement = (
            select(Project)
            .where(Project.deleted_at.is_(None))
        )


        if project_name is not None:
            statement = (
                statement
                .where(
                    Project.project_name.ilike(
                        f"%{project_name}%"
                    )
                )
            )


        if is_active:
            statement = (
                statement.where(
                    Project.project_status.has(
                        is_closed_status = False
                    )
                )
            )

        if project_status_id is not None:

            statement = (
                statement
                .where(
                    Project.project_status_id == project_status_id,
                )
            )

        if priority_id is not None:
            statement = (
                statement
                .where(
                    Project.priority_id == priority_id,

                )
            )

        if owner_user_id is not None:
            statement = (
                statement
                .where(
                    Project.owner_user_id == owner_user_id
                )
            )

        if team_id is not None:
            statement = (
                statement
                .where(
                    Project.team_id == team_id
                )
            )   
        

        statement = (
            statement
            .order_by(Project.project_name)
            .offset(offset)
            .limit(limit)
        )

        result = self.db.scalars(statement).all()
        return list(result)


    def cancel_project(
        self,
        project: Project,
        user_id: int
    ) -> Project:

        project.project_status_id = 6
        project.updated_by = user_id

        return project

    def remove_project(
        self, 
        project: Project,
        user_id: int
    ) -> None:

        project.deleted_at = datetime.now(UTC)
        project.updated_by = user_id
        


