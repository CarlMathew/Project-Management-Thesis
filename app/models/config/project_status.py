from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# if TYPE_CHECKING:
#     from app.models.core.project import Project


class ProjectStatus(Base):
    __tablename__ = "project_statuses"
    __table_args__ = {"schema": "config"}


    project_status_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True 
    )

    status_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    status_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    color_hex: Mapped[str] = mapped_column(
        String(7),
        nullable=True
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
   ) 

    is_closed_status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="0"
   )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
   )
    
    # projects: Mapped[list[Project]] = relationship(
    #     back_populates="project_status"
    # )