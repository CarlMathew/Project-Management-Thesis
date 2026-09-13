from fastapi import HTTPException, status

from app.models.auth.user import User
from app.models.core.team import Team
from app.models.core.projects import Project

from app.schemas.projects.projects import (
    ProjectOwnerResponse,
    ProjectResponse,
    ProjectTeamResponse,
)



def build_project_team_response(
    team: Team
) -> ProjectTeamResponse:


    return ProjectTeamResponse(
        team_name=team.team_name,
        team_lead_user_id=team.team_lead_user_id,
        description=team.description
    )


def build_project_owner_response(
    user: User
) -> ProjectOwnerResponse:

    return ProjectOwnerResponse(
        user_id = user.user_id,
        first_name = user.first_name,
        last_name = user.last_name,
        full_name= user.full_name,
        email = user.email,
        job_title = user.job_title
    )


def build_project_response(
    project: Project,
    team: Team,
    user: User
) -> ProjectResponse:

    return ProjectResponse(
        project_id=project.project_id,
        project_code = project.project_code,
        project_name = project.project_name,
        description = project.description,
        project_status_id=project.project_status_id,
        priority_id=project.priority_id,
        team=(
            build_project_team_response(team)
            if project.team is not None 
            else None
        ),
        owner=build_project_owner_response(user),
        start_date=project.start_date,
        target_end_date=project.target_end_date
    )
    
