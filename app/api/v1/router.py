from fastapi import APIRouter
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.configuration import router as config_router
from app.api.v1.routes.departments import router as department_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.teams import router as team_router
from app.api.v1.routes.team_members import router as team_member_router
from app.api.v1.routes.users import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(config_router)
router.include_router(department_router)
router.include_router(health_router)
router.include_router(team_router)
router.include_router(team_member_router)
router.include_router(user_router)
