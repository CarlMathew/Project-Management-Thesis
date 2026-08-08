from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean, 
    DateTime,
    ForeignKey,
    String
)


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


from app.db.base import Base



class Team(Base):
    __tablename__ = "teams"
    __table_args__ = {
        "schema": "core"
    }

    team_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    team_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    department_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "core.departments.department_id",
            ondelete="NO ACTION"
        ),
        nullable=True
    )

    team_lead_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=True
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime(),
        onupdate=func.sysutcdatetime()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    created_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )


    updated_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=True
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
