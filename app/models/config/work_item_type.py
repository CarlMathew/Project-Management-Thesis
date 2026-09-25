from sqlalchemy import (
    Boolean,
    Integer,
    String,
    
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class WorkItemType(Base):

    __tablename__ = "work_item_types"
    __table_args__ = {"schema": "config"}

    work_item_type_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    type_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    type_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True
    )

    code_prefix: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True
    )

    color_hex: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True
    )

    icon_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )

