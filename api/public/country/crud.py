# crud.py
from typing import Optional
from sqlmodel import Session, select
from api.public.country.models import Country

def get_country_by_name(session: Session, name: str) -> Optional[Country]:
    statement = select(Country).where(Country.name == name)
    result = session.exec(statement).first()
    return result

def create_country(session: Session, country_data: dict) -> Country:
    country = Country(**country_data)
    session.add(country)
    session.commit()
    session.refresh(country)
    return country

def get_all_countries(session: Session) -> list[Country]:
    statement = select(Country)
    results = session.exec(statement).all()
    return results
