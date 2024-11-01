from sqlmodel import Session, SQLModel, create_engine
from api.config import settings

ECHO_MODE = settings.ENV != "production"

if "sqlite" in settings.DATABASE_URI:
    connect_args = {"check_same_thread": False}  # Necesario solo para SQLite
else:
    connect_args = {}
engine = create_engine(settings.DATABASE_URI, connect_args=connect_args, echo=ECHO_MODE)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
