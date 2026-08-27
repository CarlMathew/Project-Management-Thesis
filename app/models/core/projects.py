from datetime import  datetime



from sqlalchemy import (
    BigInteger,
    Index,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Integer,

)

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 

)
from sqlalchemy.sql import func

from app.db.base import Base



class Project(Base):

    __tablename__ = "projects"
    __table_args__ = (
        Index(
            "ix_projects_priority_id_owner_user_id_team_id_target_end_date",
            "priority_id",
            "owner_user_id", 
            "team_id",
            "target_end_date"
        ),
        {"schema": "core"}
    )

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        autoincrement=True,
        primary_key=True
    )

    project_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    project_name: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable = True
    )
    
    project_status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("config.project_statuses.project_status_id"),
        nullable=False
    )

    priority_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("config.priorities.priority_id"),
        nullable=False
    )

    owner_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )
    
    team_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "core.teams.team_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=func.sysutcdatetime()
    )

    target_end_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=func.sysutcdatetime()
    )
    
    actual_end_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=func.sysutcdatetime()
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=0, 
        server_default="0"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
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

    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    ) 

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )



