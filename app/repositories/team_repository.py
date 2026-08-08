
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import false


from app.models import (
    Team
)

class TeamRepository:

    def __init__(self, db: Session):
        self.db = db

    
    def get_by_id(
        self,
        team_id: int
    ) -> Team | None:
        
        statement= (
            select(Team)
            .where(
                Team.team_id == team_id,
                Team.deleted_at.is_(None)
            )

        )

        return self.db.scalar(statement)

    
    def get_by_name(
        self,
        team_name: str
    ) -> Team | None:

        statement = (
            select(Team)
            .where(
                Team.team_name == team_name,
                Team.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)


    
    def list_teams(
        self,
        include_inactive: bool,
        offset: int,
        limit: int
    ) -> list[Team]:


        statement = select(Team)

        if not include_inactive:

            statement = (
                statement
                .where(Team.is_active == True)
                .offset(offset)
                .limit(limit)
                .order_by(Team.team_id)
            )

        
        return list(self.db.scalars(statement).all())


    def create(
        self,
        team: Team
    ) -> Team:


        self.db.add(team)
        self.db.flush()

        return team

        
        

