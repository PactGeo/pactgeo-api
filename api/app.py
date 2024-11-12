from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import Settings
from api.public import api as public_api
from api.utils.logger import logger_config

logger = logger_config(__name__)

origins = [
    "http://localhost:5173/",  # Cambia esto al dominio de tu frontend
    "https://geounity.org/",
]

def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/",
        description=settings.DESCRIPTION,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # Permite el envío de cookies
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(public_api)
    return app
