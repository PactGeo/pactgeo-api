from fastapi import APIRouter, Depends

from api.public.auth import views as auth
from api.public.user import views as users
from api.public.community import views as communities
from api.public.debate import views as debates
from api.public.tag import views as tags
from api.public.country import views as countries
from api.public.subnation import views as subnations
from api.public.cloudinary import views as cloudinary
from api.public.poll import views as polls
from api.public.opinion import views as opinions
from api.public.dependencies import JWTBearer, get_current_user

api = APIRouter()

api.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)
api.include_router(
    communities.router,
    prefix="/communities",
    tags=["Communities"],
)
api.include_router(
    debates.router,
    prefix="/debates",
    tags=["Debates"],
)
api.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)
api.include_router(
    tags.router,
    prefix="/tags",
    tags=["Tags"],
)
api.include_router(
    countries.router,
    prefix="/countries",
    tags=["Countries"],
)
api.include_router(
    subnations.router,
    prefix="/subnations",
    tags=["Subnations"],
)
api.include_router(
    cloudinary.router,
    prefix="/cloudinary",
    tags=["Cloudinary"],
)
api.include_router(
    polls.router,
    prefix="/polls",
    tags=["Polls"],
)
api.include_router(
    opinions.router,
    prefix="/opinions",
    tags=["Opinions"],
)
