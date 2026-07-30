from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, utc_now_naive
from app.models import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas import (
    UserCreate,
    UserUpdate
)


class UserService:
    
    def __init__(self, db: Session):

        self.db = db
        self.user_repository = UserRepository(db)

    def create_user(
        self,
        *,
        payload: UserCreate,
        created_by: int
    ) -> User:

        normalized_email = str(payload.email).strip().lower()


        if self.user_repository.email_exist(normalized_email=normalized_email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail = "A user with this email already exists."
            )
        
        unique_role_ids = list(set(payload.role_ids))

        roles = self.user_repository.get_active_roles_by_ids(
            unique_role_ids
        )

        if len(roles) != len(unique_role_ids):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "One or more selected roles do not exist or inactive"
            )


        user = User(
            email=normalized_email,
            password_hash=hash_password(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            job_title=payload.job_title,
            department_id = payload.department_id,
            is_active=True,
            created_by = created_by
        )

        try:
            self.user_repository.create_user(user)

            for role in roles:
                self.user_repository.add_role(
                    user_id = user.user_id,
                    role_id = role.role_id,
                    assigned_by = created_by
                )
            self.db.commit()
            self.db.refresh(user)
        
        
        except Exception:
            self.db.rollback()
            raise


        
        created_user = self.user_repository.get_by_id(
            user.user_id
        )

        if created_user is None:
            raise RuntimeError("User was created but cannot be retreived")
        
        return created_user


    def get_user(
        self,
        user_id: int
    ) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found. Please ask the administrator"
            )

        return user

    
    def list_users(
        self,
        *,
        offset: int,
        limit: int
    ) -> list[User]:
        return self.user_repository.get_list_users(
            offset=offset, 
            limit=limit
        )


    def update_user(
        self,
        *,
        user_id: int,
        payload: UserUpdate,
        updated_by: int
    ) -> User:
        
        user = self.get_user(user_id)

        update_data = payload.model_dump(
            exclude_unset=True
        )
 

        for field_name, value in update_data.items():

            if isinstance(value, str) and field_name != "roles_id":
                value = value.strip()

            setattr(user, field_name, value)
        
        user.updated_by = updated_by
        
   
        if payload.role_ids:
            self.user_repository.delete_role(user=user)

            unique_role_ids = list(set(payload.role_ids))

            roles = self.user_repository.get_active_roles_by_ids(
                unique_role_ids
            )

            if len(roles) != len(unique_role_ids):
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "One or more selected roles do not exist or inactive"
                )

            for role in roles:
                self.user_repository.add_role(
                    user_id = user.user_id,
                    role_id = role.role_id,
                    assigned_by = updated_by                
                )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user



    def deactivate_user(
        self,
        *,
        user_id: int,
        deactivated_by: int
    ) -> User:

        if user_id == deactivated_by:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactive your own account"
            )
        

        user: User | None = self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please ask administrator"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="User is already inactive"
            )

        user.is_active = False
        user.updated_by = deactivated_by
        user.updated_at = utc_now_naive()

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)


        return user
        

    def activate_user(
        self,
        *,
        user_id: int,
        activated_by: int
    ) -> User:


        if user_id == activated_by:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot activate a own account"
            )
        
        user: User | None = self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if user.is_active:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="User is already active"
            )


        user.is_active = True
        user.updated_by = activated_by
        user.updated_at = utc_now_naive()

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)


        return user




        
            




