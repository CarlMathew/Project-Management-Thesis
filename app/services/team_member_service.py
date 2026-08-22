from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import (
    TeamMember,
    User
)

from app.schemas import (
    AddMember,
    UpdateMember
)

from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.user_repository import UserRepository
from app.repositories.team_repository import TeamRepository


class TeamMemberService:

    def __init__(self, db: Session):
        self.db = db
        self.team_repository = TeamRepository(db)
        self.team_member_repository = TeamMemberRepository(db)
        self.user_repository = UserRepository(db)


    def add_member(
        self,
        added_by: int,
        payload: AddMember,

    ) -> TeamMember:
        
        """Add members into a project"""


        user = self.user_repository.get_by_id(payload.user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = "User does not exist or inactive"
            )
        
        team = self.team_repository.get_by_id(payload.team_id)

        if team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = "Team does not exist or inactive"
            )
        

        if self.team_member_repository.member_exists(
            payload.team_id,
            payload.user_id
        ):
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail="User already belongs to this team"
            )
        
        team_member = TeamMember(
            team_id = payload.team_id,
            user_id = payload.user_id,
            member_role = payload.member_role,
            capacity_percentage = payload.capacity_percentage,
            added_by = added_by
        )

        try:
            self.team_member_repository.add_member(team_member)
            self.db.commit()
            self.db.refresh(team_member)

            return team_member
        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team could not be created because of conflict"
            ) from exc 
        



    def list_members(
        self,
        team_id: int   
    ) -> dict[int, User]:

        team_members = self.team_member_repository.list_members(
            team_id=team_id
        )

        user_ids = set(member.user_id for member in team_members)

        users_by_ids = self.user_repository.get_users_by_ids(user_ids)

        return users_by_ids


    def get_member_by_id(
        self, 
        team_member_id: int
    ) -> TeamMember:

        team_member = self.team_member_repository.get_team_member_by_id(
            team_member_id=team_member_id
        )

        if team_member is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Team Member is not active or doesn't exist"
            )
        
        return team_member


    def update_members(
        self,
        payload: UpdateMember,
        team_member_id: int,
    ) -> TeamMember:

        team_member = (
            self
            .team_member_repository
            .get_team_member_by_id(
                team_member_id=team_member_id
            )
        )


        if team_member is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Team Member is not active or doesn't exist"
            )

        
        update_data = payload.model_dump(
            exclude_unset = True
        )

        if "member_role" in update_data:
            member_role = update_data.get("member_role", None)

            if member_role == team_member.member_role:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = f"Team member has the same role"
                )

        
        for field_name, value in update_data.items():
            setattr(team_member, field_name, value)

        
        try:
            self.db.add(team_member)
            self.db.commit()
            self.db.refresh(team_member)
            return team_member
        
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"The team could not be created because of conflict"
            ) from exc 
        


    def remove_member(
        self,
        team_member_id: int,

    ) -> TeamMember:



        team_member = (
            self
            .team_member_repository
            .get_team_member_by_id(
                team_member_id=team_member_id
            )
        )


        if team_member is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Team Member is not active or doesn't exist"
            )


        return self.team_member_repository.remove_member(
            team_member=team_member
        )


    





    



        

        

