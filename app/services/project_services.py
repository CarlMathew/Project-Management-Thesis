from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.models import (
    Project,
    User,
    Team
)


from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
)
from app.repositories.team_repository import TeamRepository
from app.repositories.configuration_repository import ConfigurationRepository
from app.repositories.project_repositories import ProjectRepository


class ProjectService:

    def __init__(self, db: Session):

        self.db = db
        self.project_repository = ProjectRepository(db) 
        self.team_repository = TeamRepository(db)
        self.configuration_repository = ConfigurationRepository(db)


    def cancel_project(
        self,
        project_id: int,
        cancel_by: int
    ) -> Project:

        project = self.project_repository.get_by_id(project_id=project_id)

        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project doesn't exist or already remove"
            )

        try:
            project = self.project_repository.cancel_project(
                project=project, 
                user_id=cancel_by
            )
            self.db.commit()
            self.db.refresh(project)
            return project

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Project can't be created. Conflicting Records"
            ) from exc



    
    def create_project(
        self,
        payload: ProjectCreate,
        owner_id: int
    ) -> Project:

            
        standardized_proj_name = payload.project_name.strip().lower()
        existing_project = self.project_repository.get_by_project_name(standardized_proj_name)

        if existing_project is not None:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail = "This Project already exist or it's on the archived"
            )

        
        self._validate_project(
            payload.team_id,
            payload.priority_id, 
            payload.project_status_id
        )

        project  = Project(
            project_name = standardized_proj_name,
            description = payload.description,
            team_id = payload.team_id,
            priority_id = payload.priority_id,
            project_status_id = payload.project_status_id,
            owner_user_id = owner_id,
            created_by= owner_id,
            start_date = payload.start_date,
            target_end_date = payload.target_end_date
        )

        try:
            self.project_repository.create(project)

            year_month = datetime.now().strftime("%y%m")
            project.project_code = f"PRJ-{year_month}-{project.project_id:05d}"

            self.db.commit()
            self.db.refresh(project)
            
            return project

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Project can't be created. Conflicting Records"
            ) from exc

    def get_owner_project(
        self,
        project_id: int
    ) -> User:

        project = self.project_repository.get_by_id(project_id=project_id)
        
        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project doesn't exist or already remove"
            )


        owner = self.project_repository.get_owner(
            project_id=project.project_id
        )

        return owner

    def get_team_project(
        self,
        project_id: int,
    ) -> Team | None:

        project = self.project_repository.get_by_id(project_id=project_id)
        
        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project doesn't exist or already remove"
            )


        team = self.project_repository.get_team(
            project_id=project.project_id
        )

        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The project does not have an assigned team."
            )

        return team
    
    def list_projects(
        self,
        project_name: str | None = None,
        project_status_id: int | None = None,
        priority_id: int | None = None, 
        owner_user_id: int | None = None,
        team_id: int | None = None,
        is_active: bool = True,
        offset: int = 0,
        limit: int = 50
    ) -> list[Project]:

        projects = self.project_repository.list_projects(
            project_name = project_name,
            project_status_id=project_status_id,
            priority_id=priority_id,
            owner_user_id=owner_user_id,
            team_id=team_id,
            is_active=is_active,
            offset=offset,
            limit=limit
        )


        return projects



    
    def update_project(
        self,
        project_id: int,
        payload: ProjectUpdate,
        updated_by: int
    ) -> Project:

        project = self.project_repository.get_by_id(project_id=project_id)

        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project doesn't exist or deleted."
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )


        if "project_name" in update_data:

            standardize_project_name = update_data["project_name"].strip().lower()
            update_data["project_name"] = standardize_project_name


            existing_project_name = self.project_repository.get_by_project_name(standardize_project_name)

            if (
                existing_project_name and
                existing_project_name.project_id != project.project_id
            ):
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = f"A project with this name already exist."
                )
            

        
        self._validate_project(
            payload.team_id,
            payload.priority_id,
            payload.project_status_id
        )

        update_data["updated_by"] = updated_by
        for field_name, value in update_data.items():
            setattr(project, field_name, value)

        try:

            self.db.commit()
            self.db.refresh(project)

            return project

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail=f"Project can't be updated. Conflicting Records"
            ) from exc


    def remove_project(
        self,
        project_id: int,
        removed_by: int
    ) -> None:
    
        project = self.project_repository.get_by_id(project_id=project_id)

        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Project doesn't exist or already remove"
            )
            
        try:
            self.project_repository.remove_project(
                project=project,
                user_id=removed_by
            )   
            self.db.commit()

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail= f"Problem on deleting the project. Conflict reasons."
            ) from exc


    def _validate_project(
        self, 
        team_id: int | None,
        priority_id: int | None,
        project_status_id: int | None
    ) -> None:

        if team_id is not None:
            team = self.team_repository.get_by_id(team_id)
            if team is None:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail = "Team does not exist or inactive."
                )


        if priority_id is not None:
            priority_status = self.configuration_repository.get_priority_id(priority_id)
            if priority_status is None:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail = "Priority Config does not exist on the database."
                )
        
        if project_status_id is not None:
            project_status = self.configuration_repository.get_project_status_id(project_status_id)

            if project_status is None:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail = "Project Status Configuration does not exist on the database."
                )
            



