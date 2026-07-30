from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# if TYPE_CHECKING:
#     from app.models.core.project import Project
#     from app.models.core.task import Task


class Priority(Base):
    __tablename__ = "priorities"
    __table_args__ = {"schema": "config"}

    priority_id:  Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    priority_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    priority_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    
    priority_level: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        unique=True
    )

    color_hex: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )

    # projects: Mapped[list[Project]] = relationship(
    #     back_populates="priority"
    # )

    # task: Mapped[list[Task]] = relationship(
    #     back_populates="priority"
    # )
