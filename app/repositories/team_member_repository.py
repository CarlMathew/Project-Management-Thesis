from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload


from app.models import (
    TeamMember,
)




class TeamMemberRepository:

    def __init__(self, db: Session):\
        self.db = db
    

    def get_team_member_by_id(
        self,
        team_member_id: int
    ) -> TeamMember | None:

        statement = (
            select(TeamMember)
            .where(
                TeamMember.team_member_id == team_member_id,
                TeamMember.is_active == True
            )
        )

        return self.db.scalar(statement)

    def member_exists(
        self,
        team_id: int,
        user_id: int
    ) -> bool:


        statement = (
            select(TeamMember)
            .where(
                TeamMember.user_id == user_id,
                TeamMember.team_id == team_id,
                TeamMember.is_active == True
            )
            .limit(1)
        )

        return self.db.scalar(statement) is not None

    # def add_member(
    #     self,
    #     team_member: TeamMember
    # ) -> TeamMember:

    #     self.db.add(team_member)
    #     return team_member


    def list_members(
        self,
        team_id: int
    ) -> list[TeamMember] | None:


        statement = (
            select(TeamMember)
            .options(joinedload(TeamMember.user))
            .where(
                TeamMember.team_id == team_id,
                TeamMember.is_active == True
            )
        )

        return list(self.db.scalars(statement).all())
    

    def remove_member(
        self,
        team_member: TeamMember,
    ) -> TeamMember:

        team_member.is_active = False
        team_member.left_at = datetime.now(UTC)

        return team_member 

        

    







