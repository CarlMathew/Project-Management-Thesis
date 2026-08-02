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

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "core"}

    department_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    department_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    manager_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "auth.users.user_id",
            ondelete="NO ACTION"
        ),
        nullable=True
    )

    supervisor_user_id: Mapped[int | None] = mapped_column(
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
        server_default=func.sysutcdatetime()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.sysutcdatetime(),
        server_default=func.sysutcdatetime()
    )