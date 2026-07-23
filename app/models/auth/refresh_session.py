from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID as PyUUID, uuid4


from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index, 
    String,

)

from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


if TYPE_CHECKING:
    from app.models import User


class RefreshSession(Base):
    __tablename__ = "refresh_sessions"
    __table_args__ = (
        Index(
            "ix_refresh_sessions_user_id_revoked_at",
            "user_id",
            "revoked_at"
        ),
        {"schema":"auth"}
    )


    refresh_session_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    session_family_id: Mapped[PyUUID] = mapped_column(
        UNIQUEIDENTIFIER,
        nullable=False,
        default=uuid4, 
        index=True
    )

    token_id: Mapped[PyUUID] = mapped_column(
        UNIQUEIDENTIFIER,
        nullable=False,
        unique=True,
        default=uuid4
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=False,
        index=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    revoked_at: Mapped[datetime | None ] = mapped_column(
        DateTime,
        nullable=True
    )

    replaced_by_token_id: Mapped[PyUUID | None] = mapped_column(
        UNIQUEIDENTIFIER,
        nullable=True
    ) 


    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    user: Mapped[User] = relationship(
        foreign_keys=[user_id]
    )

    user_agent: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )
    @property
    def is_revoked(self) -> bool: 
        return self.revoked_at is not None

