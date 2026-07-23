from datetime import date, datetime
from uuid import UUID


from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import RefreshSession

class RefreshSessionRepository:

    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create(
        self,
        *,
        user_id:int,
        session_family_id: UUID,
        token_id: UUID,
        token_hash: str,
        expires_at: datetime,
        ip_address: str | None,
        user_agent: str | None
    ) -> RefreshSession:

        refresh_session = RefreshSession(
            user_id = user_id,
            session_family_id = session_family_id,
            token_id= token_id,
            token_hash = token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )

        self.db.add(refresh_session)
        self.db.flush()

        return refresh_session
    
    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshSession | None:

        statement = select(RefreshSession).where(RefreshSession.token_hash == token_hash)

        return self.db.scalar(statement)


    def active_sessions_by_user(
        self,
        user_id: int
    ) -> list[RefreshSession]:
        statement = (
            select(RefreshSession).where(
                RefreshSession.user_id == user_id,
                RefreshSession.revoked_at.is_(None)
            )
            .order_by(RefreshSession.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    
    def get_active_session_by_id(
        self,
        *,
        refresh_session_id: int,
        user_id: int
    ) -> RefreshSession | None:
        statement = select(RefreshSession).where(
            RefreshSession.refresh_session_id == refresh_session_id,
            RefreshSession.user_id == user_id,
            RefreshSession.revoked_at.is_(None)
        )

        return self.db.scalar(statement)



    def revoke_session(
        self,
        refresh_session: RefreshSession,
        revoked_at: datetime,
    ) -> None:
        refresh_session.revoked_at = revoked_at
        self.db.add(refresh_session)

    
    def revoke_family(
        self,
        *,
        session_family_id: UUID,
        revoked_at: datetime
    ) -> None:
        statement = (
            update(RefreshSession).where(
                RefreshSession.session_family_id == session_family_id,
                RefreshSession.revoked_at.is_(None)
            )
            .values(revoked_at = revoked_at)
        )

        self.db.execute(statement)

    def revoke_all_for_users(
        self,
        *,
        user_id: int,
        revoked_at: datetime
    ) -> None:
        statement = (
            update(RefreshSession).where(
                RefreshSession.user_id == user_id,
                RefreshSession.revoked_at.is_(None)
            )
            .values(revoked_at=revoked_at)
        )

        self.db.execute(statement)