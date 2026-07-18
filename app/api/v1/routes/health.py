from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/health", tags =["Health"])

@router.get("")
def get_health() -> dict[str, str]:
    return {
        "status": "healthy", 
        "service": "project-management-system-api",
        "timestamp": datetime.now(UTC).isoformat()
    }

@router.get("/readiness")
def get_readiness(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        database_name = db.execute(
            text("SELECT DB_NAME()")
        ).scalar_one()

        return {
            "status": "ready",
            "database": str(database_name),
            "timestamp": datetime.now(UTC).isoformat()
        }
    
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is unavailable"
        )