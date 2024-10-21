# view.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.public.subdivision.models import Subdivision
from api.public.subdivision.crud import get_subdivision_by_name, create_subdivision, get_all_subdivision
from api.database import get_session

router = APIRouter()

@router.get("/", response_model=list[Subdivision])
def read_subdivision(db: Session = Depends(get_session)):
    return get_all_subdivision(db)

@router.post("/", response_model=Subdivision, status_code=status.HTTP_201_CREATED)
def create_new_subdivision(subnation_data: Subdivision, session: Session = Depends(get_session)):
    existing_subnation = get_subdivision_by_name(session, subnation_data.name)
    if existing_subnation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El país ya existe en la base de datos."
        )
    return create_subdivision(session, subnation_data.dict())
