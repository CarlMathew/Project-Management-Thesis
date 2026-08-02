from sqlalchemy import func, select
from sqlalchemy.orm import Session


from app.models import (
    Department,
    User
)


class DepartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_department_by_id(
        self,
        department_id: int
    ) -> Department | None:


        statement = (
            select(Department)
            .where(
                Department.department_id == department_id
            )
        )

        return self.db.scalar(statement)
    
    def get_department_by_name(
        self,
        department_name:str
    ) -> Department | None:

        normalized_name = department_name.lower().strip()

        statement = (
            select(Department)
            .where(
                func.lower(Department.department_name) == normalized_name
            )
        )

        return self.db.scalar(statement)

    def list_departments(
        self,
        include_inactive: bool,
        offset: int,
        limit: int
    ) -> list[Department]:

        statement = select(Department)

        if not include_inactive:
            statement = (
                statement
                .where(Department.is_active == True)
            )
        

        statement_final = (
            statement
            .order_by(Department.department_name)
            .offset(offset)
            .limit(limit)
        )

        return list(self.db.scalars(statement_final).all())


    def list_department_users(
        self,
        *,
        department_id: int,
        include_inactive: bool,
        offset: int,
        limit: int
    ) -> list[User]:

        statement = select(User)

        if not include_inactive:
            statement = (
                select(User)
                .where(
                    User.department_id == department_id,
                    User.is_active == True
                )
            )

        statement = (
            statement
            .order_by(User.last_name)
            .offset(offset)
            .limit(limit)
        )


        return list(self.db.scalars(statement).all())


    def create(
        self,
        department: Department
    ) -> Department:

        self.db.add(department)
        self.db.flush()


        return department