# view.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.public.country.models import Country
from api.public.country.crud import get_country_by_name, create_country, get_all_countries
from api.database import get_session 

router = APIRouter()

@router.get("/", response_model=list[Country])
def read_countries(db: Session = Depends(get_session)):
    return get_all_countries(db)

@router.post("/", response_model=Country, status_code=status.HTTP_201_CREATED)
def create_new_country(country_data: Country, session: Session = Depends(get_session)):
    existing_country = get_country_by_name(session, country_data.name)
    if existing_country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El país ya existe en la base de datos."
        )
    return create_country(session, country_data.dict())
