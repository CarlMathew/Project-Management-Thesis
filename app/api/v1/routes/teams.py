from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_permission
from app.db.session import get_db
from app.models import User
from app.api.dependencies.team import build_team_response
from app.schemas.teams.team import (
    TeamCreate,
    TeamResponse,
    TeamUpdate
)
from app.services.team_services import TeamService



router = APIRouter(
    prefix="/team",
    tags=["Teams"]
)



TeamViewer = Annotated[
    User,
    Depends(require_permission("team.view"))
]

TeamManager = Annotated[
    User,
    Depends(require_permission("team.manage"))
]



@router.post(
    "",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED
)
def create_team(
    payload: TeamCreate,
    current_user: TeamManager,
    db: Annotated[Session, Depends(get_db)]
)-> TeamResponse:

    team_service = TeamService(db)

    team = team_service.create_team(
        payload=payload,
        created_by=current_user.user_id
    )

    departments_by_id, users_by_id = team_service.get_team_related_records(
        [team]
    )

    return build_team_response(
        team=team,
        department_ids=departments_by_id,
        user_ids=users_by_id
    )


@router.get(
    "",
    response_model=list[TeamResponse]
)
def list_teams(
    current_user: TeamViewer,
    db: Annotated[Session, Depends(get_db)],
    include_inactive: bool = False,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50
) -> list[TeamResponse]:


    team_service = TeamService(db)

    teams = team_service.list_teams(
        include_inactive=include_inactive,
        offset=offset,
        limit=limit
    )

    departments_by_id, users_by_id = team_service.get_team_related_records(
        teams
    )

    return [
        build_team_response(
            team=team,
            department_ids=departments_by_id,
            user_ids=users_by_id
        )
        for team in teams
    ]

@router.get(
    '/{team_id}',
    response_model=TeamResponse
)
def get_team(
    team_id: int,
    current_user: TeamViewer,
    db: Annotated[Session, Depends(get_db)]
) -> TeamResponse:

    team_service = TeamService(db)

    team = team_service.get_team(team_id)

    departments_by_id, users_by_id = team_service.get_team_related_records(
        [team]
    )

    return build_team_response(
        team=team,
        department_ids=departments_by_id,
        user_ids=users_by_id
    )


@router.patch(
    '/{team_id}',
    response_model=TeamResponse
)
def update_team(
    team_id: int,
    payload: TeamUpdate,
    current_user: TeamViewer,
    db: Annotated[Session, Depends(get_db)]
) -> TeamResponse:

    team_service = TeamService(db)

    team = team_service.update_team(
        team_id=team_id,
        payload=payload,
        updated_by=current_user.user_id
    )

    departments_by_id, users_by_id = team_service.get_team_related_records(
        [team]
    )

    return build_team_response(
        team=team,
        department_ids=departments_by_id,
        user_ids=users_by_id
    )

@router.post(
    "/activate/{team_id}",
    response_model=TeamResponse
)
def activate_team(
    team_id:int,
    current_user: TeamManager,
    db: Annotated[Session, Depends(get_db)]
) -> TeamResponse:

    team_service = TeamService(db)
    
    team = team_service.activate_team(
        team_id=team_id,
        updated_by=current_user.user_id
    )


    departments_by_id, users_by_id = team_service.get_team_related_records(
        [team]
    )

    return build_team_response(
        team=team,
        department_ids=departments_by_id,
        user_ids=users_by_id
    )




@router.post(
    "/deactivate/{team_id}",
    response_model=TeamResponse
)
def deactivate_team(
    team_id:int,
    current_user: TeamManager,
    db: Annotated[Session, Depends(get_db)]
) -> TeamResponse:

    team_service = TeamService(db)
    
    team = team_service.deactivate_team(
        team_id=team_id,
        updated_by=current_user.user_id
    )


    departments_by_id, users_by_id = team_service.get_team_related_records(
        [team]
    )

    return build_team_response(
        team=team,
        department_ids=departments_by_id,
        user_ids=users_by_id
    )