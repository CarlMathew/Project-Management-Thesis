from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,

)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

if TYPE_CHECKING:

    from app.models.auth.permission import RolePermission
    from app.models.auth.user import User



class Role(Base):

    """Role Table for the app."""
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}


    role_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    role_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    is_system_role: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default= False,
        server_default="0"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default = True,
        server_default="1"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime(),
        onupdate=func.sysutcdatetime()
    )

    user_roles: Mapped[list[UserRole]] = relationship(
        back_populates="role",
        lazy="selectin"
    )

    role_permissions: Mapped[list[RolePermission]] = relationship(
        back_populates="role",
        lazy="selectin"
    )

class UserRole(Base):
    """User Roles, one user can have multiple role."""
    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role_id",
            name="uq_user_roles_user_id_role_id"
        ),
        {"schema": "auth"}
    )

    user_role_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.role_role_id"),
        nullable=False
    )

    assigned_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    user: Mapped[User] = relationship(
        back_populates="user_roles",
        foreign_keys=[user_id]
    )

    role: Mapped[Role] = relationship(
        back_populates="user_roles"
    )
    
    




