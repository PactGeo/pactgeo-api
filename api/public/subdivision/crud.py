# crud.py
from typing import Optional
from sqlmodel import Session, select
from api.public.subdivision.models import Subdivision

def get_subdivision_by_name(session: Session, name: str) -> Optional[Subdivision]:
    statement = select(Subdivision).where(Subdivision.name == name)
    result = session.exec(statement).first()
    return result

def create_subdivision(session: Session, subdivision_data: dict) -> Subdivision:
    subdivision = Subdivision(**subdivision_data)
    session.add(subdivision)
    session.commit()
    session.refresh(subdivision)
    return subdivision

def get_all_subdivision(session: Session) -> list[Subdivision]:
    statement = select(Subdivision)
    results = session.exec(statement).all()
    return results
