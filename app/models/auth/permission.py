from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,

)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.auth.role import Role
    from app.models.auth.permission import Permission


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "auth"}


    permission_id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True
    )

    permission_code: Mapped[str] = mapped_column(
        String(150),
        nullable=False, 
        unique=True 
    )

    permission_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    role_permissions: Mapped[list[RolePermission]] = relationship(
        back_populates="permission",
        lazy="selectin"
    )


class RolePermission(Base):
    """Roles can have multiple permission"""

    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permissions_role_id_permission_id"
        ),
        {"schema": "auth"}
    )
    
    role_permission_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth.roles.role_id"),
        nullable=False
    )

    permission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth.permissions.permission_id"),
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )


    role: Mapped[Role] = relationship(
        back_populates="role_permissions"
    )

    permission: Mapped[Permission] = relationship(
        back_populates="role_permissions"
    )








