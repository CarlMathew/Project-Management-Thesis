from typing import Annotated

from app.services.team_member_service import TeamMemberService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_permission
from app.api.dependencies.team_member import build_member_user_response, build_team_member_user_response
from app.db.session import get_db
from app.models import (
    User,
)

from app.services.user_service import UserService
from app.schemas import (
    TeamMemberUserResponse,
    AddMember,
    UpdateMember,
    MessageResponse
)


router = APIRouter(
    prefix="/team_member",
    tags=["Team Member"]
)


TeamMemberManager = Annotated[
    User,
    Depends(require_permission("team.manage_members"))
]

TeamMemberViewer = Annotated[
    User,
    Depends(require_permission("team.view_members"))
]



@router.post(
    "",
    response_model=TeamMemberUserResponse,
    status_code=status.HTTP_201_CREATED
)
def add_member(
    payload: AddMember,
    current_user: TeamMemberManager,
    db: Annotated[Session, Depends(get_db)]
) -> TeamMemberUserResponse:

    team_member_service = TeamMemberService(db)
    user_service = UserService(db)

    team_member = team_member_service.add_member(
        added_by=current_user.user_id,
        payload=payload
    )

    user = user_service.get_user(team_member.user_id)

    return build_team_member_user_response(
        team_member=team_member,
        user=user
    )


@router.get(
    "/members/{member_id}",
    response_model=TeamMemberUserResponse,
)
def get_member(
    member_id: int,
    current_user: TeamMemberViewer,
    db: Annotated[Session, Depends(get_db)]
) -> TeamMemberUserResponse:

    team_member_service = TeamMemberService(db)
    user_service = UserService(db)
    team_member = team_member_service.get_member_by_id(
        team_member_id=member_id
    )
    user = user_service.get_user(user_id=team_member.user_id)
    return build_team_member_user_response(
        team_member=team_member,
        user=user
    )
    
@router.get(
    "/{team_id}",
    response_model=list[TeamMemberUserResponse]
)
def list_members(
    team_id: int,
    current_user: TeamMemberViewer,
    db: Annotated[Session, Depends(get_db)]
) -> list[TeamMemberUserResponse]:

    team_member_service = TeamMemberService(db)

    members= team_member_service.list_members(
        team_id=team_id
    )

    return [
        build_member_user_response(
            member=member
        )
        for member in members
    ]


@router.patch(
    "/members/{team_member_id}",
    response_model=TeamMemberUserResponse
)
def update_member(
    team_member_id: int,
    payload: UpdateMember,
    current_user: TeamMemberManager,
    db: Annotated[Session, Depends(get_db)]
) -> TeamMemberUserResponse:
    

    team_member_service = TeamMemberService(db)
    user_service = UserService(db)

    update_member = team_member_service.update_member(
        payload=payload,
        team_member_id=team_member_id
    )

    user = user_service.get_user(update_member.user_id)

    return build_team_member_user_response(
        team_member=update_member,
        user=user
    )


@router.delete(
    "/members/{team_member_id}",
    response_model=MessageResponse
)
def remove_member(
    team_member_id: int,
    current_user: TeamMemberManager,
    db: Annotated[Session, Depends(get_db)]
) -> MessageResponse:

    team_member_service = TeamMemberService(db)

    team_member_service.remove_member(
        team_member_id=team_member_id
    )


    return MessageResponse(
        message="Membewr successfully remove from the team"
    )


