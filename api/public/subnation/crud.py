# crud.py
from typing import Optional
from sqlmodel import Session, select
from api.public.subnation.models import Subnation

def get_subnation_by_name(session: Session, name: str) -> Optional[Subnation]:
    statement = select(Subnation).where(Subnation.name == name)
    result = session.exec(statement).first()
    return result

def create_subnation(session: Session, subnation_data: dict) -> Subnation:
    subnation = Subnation(**subnation_data)
    session.add(subnation)
    session.commit()
    session.refresh(subnation)
    return subnation

def get_all_subnation(session: Session) -> list[Subnation]:
    statement = select(Subnation)
    results = session.exec(statement).all()
    return results
