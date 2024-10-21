# view.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.public.subnation.models import Subnation
from api.public.subnation.crud import get_subnation_by_name, create_subnation, get_all_subnation
from api.database import get_session

router = APIRouter()

@router.get("/", response_model=list[Subnation])
def read_subnation(db: Session = Depends(get_session)):
    return get_all_subnation(db)

@router.post("/", response_model=Subnation, status_code=status.HTTP_201_CREATED)
def create_new_subnation(subnation_data: Subnation, session: Session = Depends(get_session)):
    existing_subnation = get_subnation_by_name(session, subnation_data.name)
    if existing_subnation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El país ya existe en la base de datos."
        )
    return create_subnation(session, subnation_data.dict())
