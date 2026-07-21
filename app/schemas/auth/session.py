from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RefreshSessionResponse(BaseModel): 
    refresh_session_id: int
    created_at: datetime
    last_used_at: datetime | None
    expires_at: datetime
    ip_address: str | None
    user_agent: str | None
    is_current: bool

    model_config = ConfigDict(from_attributes=True)