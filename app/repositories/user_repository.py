
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


from app.models import UserRole, User


class UserRepository:

    """Logic Based for the user"""

    def __init__(self, db: Session) -> None:
        self.db = db


    def get_by_email(self, email: str) -> User | None:
        """Get user by email and check if it is not deleted"""
        statement = (
            select(User)
            .options(
                selectinload(User.user_roles)
                .selectinload(UserRole.role)
            )
            .where(
                User.email == email.strip().lower(),
                User.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)

    
    def get_by_id(self, user_id: int) -> User | None:
        """Get user by id and check if it is not deleted"""
        statement = (
            select(User).
            options(
                selectinload(User.user_roles).selectinload(
                    UserRole.role
                )
            ).where(
                User.user_id == user_id,
                User.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)

    
    def update_last_login(self, user: User) -> None:
        """Update the last login of a user."""

        user.last_login_at = datetime.now(UTC).replace(tzinfo=None)
        
        self.db.commit()
        self.db.refresh(user)