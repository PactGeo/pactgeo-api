from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from api.public.debate.crud import (
    create_debate,
    get_debate,
    update_debate,
    delete_debate,
    get_debates_by_type,
    add_opinion_to_debate
)
from api.public.debate.models import DebateCreate, DebateRead, DebateUpdate
from api.public.point_of_view.models import OpinionCreate, OpinionRead
from api.database import get_session
from api.public.debate.crud import get_all_debates
from api.public.dependencies import get_current_user
from api.public.user.models import User

router = APIRouter()

@router.get("/", response_model=list[DebateRead])
def read_debates(
    debate_type: Optional[str] = Query(None, description="Type of debate: GLOBAL, INTERNATIONAL, NATIONAL, SUBNATIONAL, SUBDIVISION"),
    db: Session = Depends(get_session)
):
    print('=============================')
    print(debate_type)
    if debate_type:
        return get_debates_by_type(debate_type, db)
    return get_all_debates(db)

@router.get("/global", response_model=list[DebateRead])
def read_debates_global(
    db: Session = Depends(get_session)
):
    return get_debates_by_type('GLOBAL', db)

@router.get("/{slug}", response_model=DebateRead)
def read_debate(slug: str, db: Session = Depends(get_session)):
    return get_debate(slug, db)

@router.post("/{debate_id}/opinion", response_model=OpinionRead, status_code=status.HTTP_201_CREATED)
def add_opinion(
    debate_id: int,
    opinion: OpinionCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    print('===========================add_opinion==')
    print(debate_id)
    print(opinion)
    print(current_user)
    result = add_opinion_to_debate(debate_id, opinion, db, current_user)
    return result

@router.post("/", response_model=DebateRead, status_code=status.HTTP_201_CREATED)
def create(
    debate: DebateCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_debate = create_debate(debate, db, current_user)
    return DebateRead.from_debate(db_debate, current_user.username)


@router.patch("/{debate_id}", response_model=DebateRead)
def update(
    debate_id: int, debate_update: DebateUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return update_debate(debate_id, debate_update, db, current_user)


@router.delete("/{debate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(debate_id: int, db: Session = Depends(get_session)):
    delete_debate(debate_id, db)
