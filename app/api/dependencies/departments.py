from app.models import (
    Department,
    User, 
)
from app.schemas import (
    DepartmentUserResponse,
    DepartmentResponse
)




def build_department_user_response(
    user: User | None = None
) -> DepartmentUserResponse | None:


    if user is None:
       return None
    
    return DepartmentUserResponse(
        user_id = user.user_id,
        first_name = user.first_name,
        last_name = user.last_name,
        full_name = user.full_name,
        job_title = user.job_title,
        email =  user.email
)


def build_department_response(
    department: Department,
    manager_user: User | None = None,
    supervisor_user: User | None = None
) -> DepartmentResponse:

    return DepartmentResponse(
        department_id = department.department_id,
        department_name = department.department_name,
        description = department.description,
        manager = build_department_user_response(manager_user),
        supervisor = build_department_user_response(supervisor_user),
        is_active = department.is_active,
        created_at = department.created_at,
        updated_at = department.updated_at
    )




