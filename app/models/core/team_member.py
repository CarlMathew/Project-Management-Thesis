from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING


from sqlalchemy import (
    BigInteger,
    String,
    Boolean,
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    
)

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from sqlalchemy.sql import func

from app.db.base import Base


if TYPE_CHECKING:
    from app.models.auth.user import User
    from app.models.core.team import Team


class TeamMember(Base):

    __tablename__ = "team_members"
    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "user_id",
            name="uq_team_members_team_id_user_id"
        ),
        {"schema": "core"}
    )


    team_member_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    team_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "core.teams.team_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )

    member_role: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    capacity_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5,2),
        default=Decimal("100.00"),
        nullable=False
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    left_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    ) 
    
    added_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )

    added_by_user: Mapped["User"] = relationship(
        foreign_keys=[added_by]
    )

    team: Mapped["Team"] = relationship(
        back_populates="team_members"
    )


    user: Mapped["User"] = relationship(
        back_populates="team_members",
        foreign_keys=[user_id]
    )


    


    



