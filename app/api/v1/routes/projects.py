from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.services.project_services import ProjectService
from app.api.dependencies.auth import require_permission
from app.api.dependencies.projects import build_project_owner_response, build_project_response, build_project_team_response

from app.db.session import get_db
from app.models import User
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectOwnerResponse,
    ProjectTeamResponse,
    ProjectResponse,
    MessageResponse
)


router = APIRouter(
    prefix="/project",
    tags = ["Projects"]
)

ProjectCreator = Annotated[
    User,
    Depends(require_permission("project.create"))
]

ProjectViewer = Annotated[
    User,
    Depends(require_permission("project.view"))
]


ProjectUpdater = Annotated[
    User,
    Depends(require_permission("project.update"))
]

ProjectArchiver = Annotated[
    User,
    Depends(require_permission("project.archive"))
]

ProjectCancellor = Annotated[
    User,
    Depends(require_permission("project.cancel"))
]



@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    payload: ProjectCreate,
    current_user: ProjectCreator,
    db: Annotated[Session, Depends(get_db)]
) -> ProjectResponse:
    
    project_service = ProjectService(db)

    project = project_service.create_project(
        payload=payload,
        owner_id=current_user.user_id
    )


    return build_project_response(
        project=project,
        team=project.team,
        user=project.owner
    )




@router.post(
    "/cancel/{project_id}",
    response_model = ProjectResponse
)
def cancel_project(
    project_id: int,
    current_user: ProjectCancellor,
    db: Annotated[Session, Depends(get_db)]
) -> ProjectResponse:

    project_service = ProjectService(db)

    project = project_service.cancel_project(
        project_id=project_id,
        cancel_by = current_user.user_id
    )
    return build_project_response(
        project=project,
        team=project.team,
        user=project.owner
    )


@router.get(
    "/{project_id}/owner",
    response_model=ProjectOwnerResponse
)
def get_project_owner(
    project_id: int,
    current_user: ProjectViewer,
    db: Annotated[Session, Depends(get_db)]
) -> ProjectOwnerResponse:

    project_service = ProjectService(db)

    owner = project_service.get_owner_project(project_id)

    return build_project_owner_response(user=owner)


@router.get(
    "/{project_id}/team",
    response_model=ProjectTeamResponse
)
def get_project_team(
    project_id: int,
    current_user: ProjectViewer,
    db: Annotated[Session, Depends(get_db)]
) -> ProjectTeamResponse:

    project_service = ProjectService(db)

    team = project_service.get_team_project(project_id)



    return build_project_team_response(team=team)

@router.get(
    "",
    response_model=list[ProjectResponse]
)
def list_projects(
    current_user: ProjectViewer,
    db: Annotated[Session, Depends(get_db)],
    project_name: str | None = Query(None),
    project_status_id: int | None = Query(None),
    priority_id: int | None = Query(None),
    owner_user_id: int | None = Query(None),
    team_id: int | None = Query(None),
    is_active: bool = Query(True),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> list[ProjectResponse]:
    
    project_service = ProjectService(db)

    projects = project_service.list_projects(
        project_name=project_name,
        project_status_id=project_status_id,
        priority_id=priority_id,
        owner_user_id=owner_user_id,
        team_id=team_id,
        is_active=is_active,
        offset=offset,
        limit=limit
    )

    return [
        build_project_response(
            project=project,
            team=project.team,
            user=project.owner
        )
        for project in projects
    ]

@router.delete( 
    "/{project_id}",
    response_model = MessageResponse
)
def remove_project(
    current_user: ProjectCancellor,
    project_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> MessageResponse:

    project_service = ProjectService(db)

    project_service.remove_project(
        project_id=project_id,
        removed_by=current_user.user_id
    )

    return MessageResponse(
        message="Project remove successfully."
    )


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    current_user: ProjectUpdater,
    project_id: int,
    payload: ProjectUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> ProjectResponse:

    project_service = ProjectService(db)

    project = project_service.update_project(
        project_id=project_id,
        payload=payload,
        updated_by=current_user.user_id
    )

    return build_project_response(
        project=project,
        team=project.team,
        user=project.owner
    )


