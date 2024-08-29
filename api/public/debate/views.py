from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from api.public.debate.crud import create_debate, get_debate, update_debate, delete_debate, get_debates_by_type
from api.public.debate.models import DebateCreate, DebateRead, DebateUpdate
from api.database import get_session
from api.public.debate.crud import get_all_debates

router = APIRouter()

@router.get("/", response_model=list[DebateRead])
def read_all_debates(db: Session = Depends(get_session)):
    return get_all_debates(db)

@router.get("/global", response_model=list[DebateRead])
def read_global_debates(db: Session = Depends(get_session)):
    return get_debates_by_type("global", db)

@router.get("/international", response_model=list[DebateRead])
def read_international_debates(db: Session = Depends(get_session)):
    return get_debates_by_type("international", db)

@router.get("/national", response_model=list[DebateRead])
def read_national_debates(db: Session = Depends(get_session)):
    return get_debates_by_type("national", db)

@router.get("/local", response_model=list[DebateRead])  # Cambié la ruta a "/local" para consistencia
def read_local_debates(db: Session = Depends(get_session)):
    return get_debates_by_type("local", db)


@router.post("/", response_model=DebateRead, status_code=status.HTTP_201_CREATED)
def create(debate: DebateCreate, db: Session = Depends(get_session)):
    return create_debate(debate, db)

@router.get("/{debate_id}", response_model=DebateRead)
def read(debate_id: int, db: Session = Depends(get_session)):
    return get_debate(debate_id, db)

@router.patch("/{debate_id}", response_model=DebateRead)
def update(debate_id: int, debate_update: DebateUpdate, db: Session = Depends(get_session)):
    return update_debate(debate_id, debate_update, db)

@router.delete("/{debate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(debate_id: int, db: Session = Depends(get_session)):
    delete_debate(debate_id, db)
