from app.models.auth.user import User
from app.models.core.team_member import TeamMember



from app.schemas import TeamMemberUserResponse


def build_team_member_user_response(
    team_member: TeamMember,
    user: User
) -> TeamMemberUserResponse:

    return TeamMemberUserResponse(
        team_member_id= team_member.team_id, 
        user_id= team_member.user_id,
        full_name= user.full_name,
        email = user.email,
        job_title = user.job_title,
        member_role = team_member.member_role,
        capacity_percentage= team_member.capacity_percentage
    )


def build_member_user_response(
    member: TeamMember
) -> TeamMemberUserResponse:

    return TeamMemberUserResponse(
        team_member_id= member.team_id, 
        user_id= member.user_id,
        full_name= member.user.full_name,
        email = member.user.email,
        job_title = member.user.job_title,
        member_role = member.member_role,
        capacity_percentage= member.capacity_percentage
    )

