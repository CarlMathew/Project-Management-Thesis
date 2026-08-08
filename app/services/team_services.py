from app.models.core import team
from app.repositories import team_repository
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import (
    Department, 
    User, 
    Team
)
from app.repositories.department_repository import DepartmentRepository 
from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository


from app.schemas import (
    TeamCreate, 
    TeamUpdate
)

class TeamService:

    def __init__(self, db: Session):
        self.db = db
        self.department_repository = DepartmentRepository(db)
        self.team_repository = TeamRepository(db)
        self.user_repository = UserRepository(db)

    def create_team(
        self,
        *,
        payload: TeamCreate,
        created_by: int
    ) -> Team:
        
        existing_team = self.team_repository.get_by_name(payload.team_name)

        if existing_team is not None:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "A team with this name already exists."
            )


        self._validate_department(payload.department_id)
        self._validate_team_lead(payload.team_leader_user_id)

        team = Team(
            team_name = payload.team_name,
            description=payload.description,
            department_id=payload.department_id,
            team_lead_user_id=payload.team_leader_user_id,
            is_active=True,
            created_by=created_by
        )


        try:
            self.team_repository.create(team)
            self.db.commit()
            self.db.flush()
        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team could not be created because of conflict"
            ) from exc 
        
        return team

    
    def get_team(
        self,
        team_id: int
    ) -> Team:


        team = self.team_repository.get_by_id(team_id)

        if team is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"The team does not exist or inactive"
            )

        return team
    
    def list_teams(
        self,
        *,
        include_inactive: bool,
        offset: int,
        limit: int
    ) -> list[Team]:

        teams = self.team_repository.list_teams(
            include_inactive=include_inactive,
            offset=offset,
            limit=limit
        )

        if not teams:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no teams or all teams are inactive"
            )
        
        return teams


    def update_team(
        self,
        *,
        team_id: int,
        payload:TeamUpdate,
        updated_by: int
    ) -> Team:


        team = self.team_repository.get_by_id(team_id)

                
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "The team doesn't exist or inactive"
            )

        updated_data = payload.model_dump(
            exclude_unset=True
        )

        if "team_name" in updated_data:
            existing_team = self.team_repository.get_by_name(updated_data["team_name"])

            if (
                existing_team is not None and
                existing_team.team_id != team.team_id
            ):
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = f"A team with this is already existing"
                )
            
        
        if "department_id" in updated_data:
            self._validate_department(
                updated_data["department_id"]
            )
        

        if "team_lead_user_id" in updated_data:
            self._validate_team_lead(
                updated_data["team_lead_user_id"]
            )

        
        for key, value in updated_data.items():
            setattr(team, key, value)

        team.updated_by = updated_by
        try:

            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team could not be created because of conflict"
            ) from exc 
        
        return team

    

    def activate_team(
        self, 
        team_id: int,
        updated_by: int
    ) -> Team:


        team = self.team_repository.get_by_id(team_id)

        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "The team doesn't exist or inactive"
            )

        if team.is_active:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team is already actived"
            )

        team.is_active = True
        team.updated_by = updated_by 

        try:
            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = f"Service Unavailable please ask IT"
            ) from exc

        return team



    def deactivate_team(
        self, 
        team_id: int,
        updated_by: int
    ) -> Team:


        team = self.team_repository.get_by_id(team_id)

        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "The team doesn't exist or inactive"
            )

        if not team.is_active:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team is already deactivated"
            )

        team.is_active = False
        team.updated_by = updated_by 

        try:
            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = f"Service Unavailable please ask IT"
            ) from exc

        return team

    def get_team_related_records(
        self,
        teams: list[Team]
    ) -> tuple[dict[int, Department] | None, dict[int,User] | None]:

        department_ids: set[int] = set()
        users_ids: set[int] = set()


        for team in teams:
            if team.department_id:
                department_ids.add(team.department_id)
            
            if team.team_lead_user_id:
                users_ids.add(team.team_lead_user_id)

        departments_by_ids = self.department_repository.get_departments_by_ids(
            department_ids
        ) 

        users_by_ids = self.user_repository.get_users_by_ids(
            users_ids
        )


        return departments_by_ids, users_by_ids



    def _validate_department(
        self,
        department_id: int | None
    ) -> None:

        if department_id is None:
            return

        
        department = self.department_repository.get_department_by_id(
            department_id
        )

        if department is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "The selected department does not exist or inactive."
            )


    def _validate_team_lead(
        self,
        team_leader_user_id: int | None
    ) -> None:

        if team_leader_user_id is None:
            return
        
        team_lead = self.user_repository.get_by_id(team_leader_user_id)

        if team_lead is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "The selected team lead does not exist or inactive."
            )