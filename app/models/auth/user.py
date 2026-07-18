from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


from app.db.base import Base


if TYPE_CHECKING:
    from app.models.auth.role import UserRole


class User(Base):
    """User Table in the auth schema"""
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    user_id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True, 
        index=True
    
    )
    password_hash: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    job_title: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    department_id: Mapped[int | None] = mapped_column(
        BigInteger, 
        nullable=True
    )

    profile_image_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
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
    created_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=True
    )
    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=True
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    user_roles: Mapped[list[UserRole]] = relationship(
        back_populates="user", 
        foreign_keys="UserRole.user_id",
        lazy="selectin"
    )


    @property
    def full_name(self)-> str:
        return f"{self.first_name} {self.last_name}".strip()




 