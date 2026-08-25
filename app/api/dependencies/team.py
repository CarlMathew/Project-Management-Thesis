from app.models.auth.user import User
from app.models.core.department import Department
from app.models.core.team import Team

from app.schemas import(
    TeamDepartmentResponse,
    TeamResponse,
    TeamUserResponse
)

def build_department_response(
    department: Department | None
) -> TeamDepartmentResponse | None:

    if department is None:
        return None
    

    return TeamDepartmentResponse(
        department_id=department.department_id,
        department_name=department.department_name
    )


def build_user_response(
    user: User | None
) -> TeamUserResponse | None:

    if user is None:
        return None

    return TeamUserResponse(
        user_id= user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        email=user.email,
        job_title=user.job_title

    )


def build_team_response(
    team: Team,
    department_ids: dict[int, Department] | None,
    user_ids: dict[int, User] | None
) -> TeamResponse:


    department = None
    user = None


    if department_ids is not None:
        department = department_ids.get(team.department_id)
    
    if user_ids is not None:
        user = user_ids.get(team.team_lead_user_id)


    return TeamResponse(
        team_id = team.team_id,
        team_name=team.team_name,
        team_description=team.description,
        department=build_department_response(department),
        team_lead=build_user_response(user),
        is_active=team.is_active,
        created_at=team.created_at,
        updated_at=team.updated_at
        
    )