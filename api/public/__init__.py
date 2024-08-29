from fastapi import APIRouter, Depends

from api.auth import authent
from api.public.health import views as health
from api.public.hero import views as heroes
from api.public.team import views as teams
from api.public.user import views as users
from api.public.community import views as communities
from api.public.debate import views as debates
from api.public.comment import views as comments
from api.public.tag import views as tags

api = APIRouter()

api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
    dependencies=[Depends(authent)],
)
api.include_router(
    heroes.router,
    prefix="/heroes",
    tags=["Heroes"],
    dependencies=[Depends(authent)],
)
api.include_router(
    teams.router,
    prefix="/teams",
    tags=["Teams"],
    dependencies=[Depends(authent)],
)
api.include_router(
    comments.router,
    prefix="/comments",
    tags=["Comments"],
    dependencies=[Depends(authent)],
)
api.include_router(
    communities.router,
    prefix="/communities",
    tags=["Communities"],
    dependencies=[Depends(authent)],
)
api.include_router(
    debates.router,
    prefix="/debates",
    tags=["Debates"],
    dependencies=[Depends(authent)],
)
api.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(authent)],
)
api.include_router(
    tags.router,
    prefix="/tags",
    tags=["Tags"],
    dependencies=[Depends(authent)],
)
