from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import (
    Department,
    User
)
from app.schemas import (
    DepartmentCreate, 
    DepartmentUpdate
)
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository



class DepartmentService:

    def __init__(self, db: Session):
        self.db = db
        self.department_repository = DepartmentRepository(db)
        self.user_repository = UserRepository(db)
        
    def create_department(
        self,
        payload: DepartmentCreate
    ) -> Department:

        existing_department =   self.department_repository.get_department_by_name(
            department_name= payload.department_name
        )

        if existing_department is not None:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail = "A department with this name already exists."
            )
        self._validate_leadership(
            manager_user_id=payload.manager_user_id,
            supervisor_user_id= payload.supervisor_user_id
        )

        department = Department(
            department_name = payload.department_name,
            description = payload.description or None,
            manager_user_id = payload.manager_user_id or None,
            supervisor_user_id = payload.supervisor_user_id or None,
            is_active=True
        )

        try:
            self.department_repository.create(department)
            self.db.commit()
            self.db.refresh(department)

            return department
        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail=("Department failed to be created. Conflicting Records")
            ) from exc


        
    def get_department_by_id(
        self,
        department_id: int
    ) -> Department | None:


        department = self.department_repository.get_department_by_id(department_id)

        if department is None:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Department doesn't exist."
            )
        
        return department
    

    def list_departments(
        self,
        include_inactive: bool,
        offset: int,
        limit: int
    ) -> list[Department]:

        departments = self.department_repository.list_departments(
            include_inactive,
            offset,
            limit
        )

        if not departments:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "No department has been created"
            )

        return departments

        
    def list_department_users(
        self,
        *,
        department_id: int, 
        include_inactive: bool,
        offset:int,
        limit: int
    ) -> list[User] | None:

        users = self.department_repository.list_department_users(
            department_id=department_id,
            include_inactive=include_inactive,
            offset=offset,
            limit=limit
        )

        return users

    
    def get_deparments_leaders(
        self,
        departments: list[Department]
    ) -> dict[int, User]:

        user_ids: set[int] = set()

        for department in departments:
            
            if department.manager_user_id is not None:
                user_ids.add(
                    department.manager_user_id
                )
            
            if department.supervisor_user_id is not None:
                user_ids.add(
                    department.supervisor_user_id
                )
        
        return self.user_repository.get_users_by_ids(
            user_ids
        )


    def update_department(
        self,
        *,
        department_id: int,
        payload: DepartmentUpdate
    ) -> Department:
        
        department = self.department_repository.get_department_by_id(department_id)

        if department is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Department cannot be found. Please ask the admin."
            )
        
        update_data = payload.model_dump(
            exclude_unset = True
        )

        if "department_name" in update_data:

            existing_department = (
                self.department_repository.get_department_by_name(
                    update_data["department_name"]
                )
            )

            if (
                existing_department is not None
                and existing_department.department_id != department.department_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A department with this name already exists."
                )
        

        final_manager_user_id = update_data.get(
            "manager_user_id",
            department.manager_user_id
        )

        final_supervisor_user_id = update_data.get(
            "supervisor_user_id",
            department.supervisor_user_id
        )

        self._validate_leadership(
            manager_user_id= final_manager_user_id,
            supervisor_user_id= final_supervisor_user_id
        )


        for field_name, value in update_data.items():
            setattr(department, field_name, value)


        try:
            self.department_repository.create(department)
            self.db.commit()
            self.db.refresh(department)
            
            return department
        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                details=("Department failed to be created. Conflicting Records")
            ) from exc



    def activate_department(
        self,
        department_id: int
    ) -> Department | None:

        department = self.department_repository.get_department_by_id(department_id)

        if department is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Department does not exist."
            )
        

        if department.is_active:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Department is already active"
            )
            

        department.is_active = True
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)

        return department

    def deactivate_department(
        self,
        department_id: int
    ) -> Department | None:


        department = self.department_repository.get_department_by_id(department_id)

        if department is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Department does not exist."
            )
        

        if not department.is_active:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Department is already deactive"
            )
            

        department.is_active = False
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)

        return department

    def _validate_leadership(
        self, 
        *,
        supervisor_user_id: int | None,
        manager_user_id: int | None
    ) -> None:

        if (
            manager_user_id is not None
            and manager_user_id == supervisor_user_id
        ):
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "The manager and supervisor must be different users."
            )
        
        if manager_user_id is not None:
            manager = self.user_repository.get_by_id(manager_user_id)

            if manager is None:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Manager doesn't exist inactive"
                )
            
        
        if supervisor_user_id is not None:
            supervisor = self.user_repository.get_by_id(supervisor_user_id)

            if supervisor is None:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Supervisor doesn't exist or inactive"
                )
            
        