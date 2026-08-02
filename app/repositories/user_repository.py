
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.orm import Session, selectinload


from app.models import (
    RolePermission,
    Role,
    UserRole, 
    User
)



def get_user_auth_options():
    return[
        selectinload(User.user_roles)
        .selectinload(UserRole.role)
        .selectinload(Role.role_permissions)
        .selectinload(RolePermission.permission)
    ]

class UserRepository:

    """Logic Based for the user"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_role(
        self,
        *,
        user_id:int,
        role_id: int,
        assigned_by:int
    ) -> UserRole:

        new_user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by
        )

        self.db.add(new_user_role)
        self.db.flush()

    
        return new_user_role

    def delete_role(
        self,
        *,
        user: User,
    ) -> None:

        for user_role in user.user_roles:
            self.db.delete(user_role)
        user.user_roles.clear()
        self.db.flush()

        # statement = delete(UserRole).where(UserRole.user_id == user_id)
        # _ = self.db.execute(statement)

        # self.db.commit()



    def create_user(
        self,
        user: User
    ) -> User:

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        
        return user


    def email_exist(
        self,
        normalized_email: str
    ) -> bool:

        statement = (
            select(User)
            .where(
                User.email == normalized_email
            )
            .limit(1)
        )

        return bool(self.db.scalar(statement))

    def get_active_roles_by_ids(
        self,
        role_ids: list[int]
    ) -> list[Role]:
        
        if not role_ids:
            return []
        
        statement = (
            select(Role)
            .where(
                Role.role_id.in_(role_ids),
                Role.is_active == True
            )
        )

        return list(self.db.scalars(statement).all())

    def get_list_users(
        self,
        *,
        offset: int = 0,
        limit: int = 50
    ) -> list[User]:

        statement = (
            select(User)
            .options(*get_user_auth_options())
            .where(User.deleted_at.is_(None))
            .order_by(
                User.first_name,
                User.last_name
            )
            .offset(offset)
            .limit(limit)
        )

        return list(self.db.scalars(statement).unique().all())


    def get_by_email(self, email: str) -> User | None:
        """Get user by email and check if it is not deleted"""
        statement = (
            select(User)
            .options(*get_user_auth_options())
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
            options(*get_user_auth_options())
            .where(
                User.user_id == user_id,
                User.deleted_at.is_(None)
            )
        )

        return self.db.scalar(statement)

    def get_users_by_ids(
        self,
        user_ids: set[int],
    ) -> dict[int, User] | None:

        if not user_ids:
            return {}
        
        statement = (
            select(User)
            .where(
                User.user_id.in_(user_ids),
                User.deleted_at.is_(None)
            )
            
        )


        users = self.db.scalars(statement).all()

        return {
            user.user_id: user
            for user in users
        }


    def set_last_login(
        self,
        *,
        user: User,
        last_login_at: datetime
    ) -> None:

        user.last_login_at = last_login_at
        self.db.add(user)