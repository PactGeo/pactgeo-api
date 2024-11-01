from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from api.database import get_session
from api.public.dependencies import get_current_user
from api.public.point_of_view.models import OpinionVote, Opinion, OpinionVoteCreate
from api.public.user.models import User

router = APIRouter()

@router.post("/{opinion_id}/vote")
def vote_opinion(
    opinion_id: int,
    data: OpinionVoteCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    print('vote_opinion')
    print('opinion_id:', opinion_id)
    print('value:', data.value)
    print(11111)
    if data.value not in (1, -1):
        print(2222222)
        raise HTTPException(status_code=400, detail="Invalid vote value")

    print(333333)
    opinion = db.get(Opinion, opinion_id)
    print('opinion:', opinion)
    if not opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")

    # Verificar si el usuario ya votó en esta opinión
    existing_vote = db.exec(
        select(OpinionVote)
        .where(OpinionVote.opinion_id == opinion_id, OpinionVote.user_id == current_user.id)
    ).first()

    if existing_vote:
        # Actualizar el voto existente
        existing_vote.value = data.value
        existing_vote.created_at = datetime.utcnow()
        db.add(existing_vote)
    else:
        # Crear un nuevo voto
        new_vote = OpinionVote(
            opinion_id=opinion_id,
            user_id=current_user.id,
            value=data.value
        )
        db.add(new_vote)

    db.commit()
    return {"message": "Vote registered"}
