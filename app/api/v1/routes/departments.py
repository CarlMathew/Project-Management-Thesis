from typing import Annotated

from app.models.core.department import Department
from fastapi import (
    APIRouter, 
    Depends,
    Query, 

)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.dependencies.auth import require_permission
from app.api.dependencies.departments import (
    build_department_response,
    
)
from app.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,

)
from app.models import (
    User
)

from app.services.department_service import DepartmentService 
from app.services.user_service import UserService

router = APIRouter(
    prefix = "/department",
    tags=["Departments"]
)


DeparmentManager = Annotated[User, Depends(require_permission("department.manage"))]
DepartmentViewer = Annotated[User, Depends(require_permission("department.view"))]


@router.post(
    "",
    response_model = DepartmentResponse
)
def create_department(
    payload: DepartmentCreate,
    currentUser: DeparmentManager,
    db: Annotated[Session, Depends(get_db)]
) -> DepartmentResponse:


    manager = None
    supervisor = None

    user_service = UserService(db)
    department_service = DepartmentService(db)


    department = department_service.create_department(payload)


    if payload.manager_user_id is not None: 
        manager = user_service.get_user(payload.manager_user_id)

    if payload.supervisor_user_id is not None:
        supervisor = user_service.get_user(payload.supervisor_user_id)
    
    return build_department_response(
        department=department,
        manager_user=manager,
        supervisor_user=supervisor
    )


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def list_departments(
    current_user: DepartmentViewer,
    db: Annotated[Session, Depends(get_db)],
    include_inactive: bool = False,
    offset: Annotated[int, Query(ge=0)] = 0, 
    limit: Annotated[
        int, 
        Query(ge=1, le=100)
    ] = 50
) -> list[DepartmentResponse]:


    department_service = DepartmentService(db)

    departments = department_service.list_departments(
        include_inactive=include_inactive,
        limit=limit,
        offset=offset
    ) or []

    leaders_map = department_service.get_deparments_leaders(departments)

    return [
        build_department_response(
            department,
            (
                leaders_map.get(department.manager_user_id)
                if department.manager_user_id is not None
                else None
            ),
            (
                leaders_map.get(department.supervisor_user_id)
                if department.supervisor_user_id is not None
                else None

            )
        )
        for department in departments
    ]


@router.get(
    "/{department_id}",
    response_model= DepartmentResponse
)
def get_department(
    department_id: int,
    current_user: DepartmentViewer,
    db: Annotated[Session, Depends(get_db)]
) -> DepartmentResponse | None:

    department_service = DepartmentService(db)

    department =  department_service.get_department_by_id(
        department_id
    ) 

    if department is not None:
        leaders_map = department_service.get_deparments_leaders(
            [department]
        ) 
    

        return build_department_response(
                department,
                (
                    leaders_map.get(department.manager_user_id)
                    if department.manager_user_id is not None
                    else None
                ),
                (
                    leaders_map.get(department.supervisor_user_id)
                    if department.supervisor_user_id is not None
                    else None

                )
            )
    else:
        return None


@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    current_user: DeparmentManager,
    db:Annotated[Session, Depends(get_db)]
) -> DepartmentResponse:

    department_service = DepartmentService(db)

    department = department_service.update_department(
        department_id=department_id,
        payload=payload
    )

    leaders_map = department_service.get_deparments_leaders(
        [department]
    )




    return build_department_response(
            department,
            (
                leaders_map.get(department.manager_user_id)
                if department.manager_user_id is not None
                else None
            ),
            (
                leaders_map.get(department.supervisor_user_id)
                if department.supervisor_user_id is not None
                else None

            )
        )

@router.post(
    "/{department_id}/activate",
    response_model = DepartmentResponse
)
def activate_department(
    department_id: int,
    current_user: DeparmentManager,
    db: Annotated[Session, Depends(get_db)]
) -> DepartmentResponse | None:

    department_service = DepartmentService(db)

    department = department_service.activate_department(department_id)

    if department is not None:
        leaders_map = department_service.get_deparments_leaders(
            [department]
        )

        return build_department_response(
                department,
                (
                    leaders_map.get(department.manager_user_id)
                    if department.manager_user_id is not None
                    else None
                ),
                (
                    leaders_map.get(department.supervisor_user_id)
                    if department.supervisor_user_id is not None
                    else None

                )
            )
    else:
        return None


@router.post(
    "/{department_id}/deactivate",
    response_model = DepartmentResponse
)
def deactivate_department(
    department_id: int,
    current_user: DeparmentManager,
    db: Annotated[Session, Depends(get_db)]
) -> DepartmentResponse | None:

    department_service = DepartmentService(db)

    department = department_service.deactivate_department(department_id)

    if department is not None:
        leaders_map = department_service.get_deparments_leaders(
            [department]
        )

        return build_department_response(
                department,
                (
                    leaders_map.get(department.manager_user_id)
                    if department.manager_user_id is not None
                    else None
                ),
                (
                    leaders_map.get(department.supervisor_user_id)
                    if department.supervisor_user_id is not None
                    else None

                )
            )
    else:
        return None