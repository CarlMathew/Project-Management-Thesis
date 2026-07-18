from collections.abc import Generator
import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


logger = logging.getLogger(__name__)


if not settings.database_url:
    logger.error("DATABASE_URL is missing. Please provide DATABASE_URL in your .env file.")
    raise ValueError("DATABASE_URL is required but was not provided.")


logger.info("Creating database engine.")

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=settings.debug,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for the application.
    Creates a new SQLAlchemy session per request and closes it after use.
    """

    logger.debug("Opening database session.")

    try:
        with SessionLocal() as session:
            yield session

    except Exception:
        logger.exception("Database session error occurred.")
        raise

    finally:
        logger.debug("Database session closed.")