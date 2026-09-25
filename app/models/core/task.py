from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base



class Task(Base):

    __tablename__ = "tasks"


    __table_args__ = (
        Index(
            "ix_tasks_project_status",
            "project_id",
            "task_status_id"
        ),
        Index(
            "ix_tasks_type_status",
            "work_item_type_id",
            "task_status_id"
        ), 
        Index(
            "ix_tasks_project_priority",
            "project_id",
            "priority_id"
        ),
        {"schema": "core"}
    )

    task_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    task_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    work_item_type_id: Mapped[int] = mapped_column( 
        Integer,
        ForeignKey(
            (
                "config.work_item_types.work_item_type_id"
            ),
            ondelete="NO ACTION"
        ),
        nullable=False,
        index=True
    )

    project_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "core.projects.project_id",
            ondelete="NO ACTION"
        ),
        nullable=True,
        index=True
    )

    parent_task_id: Mapped[int | None] = mapped_column(
        BigInteger, 
        ForeignKey(
            "core.tasks.task_id",
            ondelete="NO ACTION"
        ),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    description: Mapped[str | None]  = mapped_column(
        Text,
        nullable=True
    )

    task_status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "config.task_statuses.task_status_id",
            ondelete="NO ACTION"
        ),

        nullable=False,
        index=True
    )

    priority_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "config.priorities.priority_id",
            ondelete="NO ACTION"
        ),
        nullable=False,
        index=True
    )

    reporter_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=False
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    estimaed_hours: Mapped[Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True
    )

    actual_hours: Mapped[Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default= func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default= func.sysutcdatetime(),
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
        nullable=True

    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
















