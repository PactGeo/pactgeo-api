from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from api.public.comment.crud import create_comment, get_comment, update_comment, delete_comment
from api.public.comment.models import CommentCreate, CommentRead, CommentUpdate
from api.database import get_session

router = APIRouter()

@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create(comment: CommentCreate, db: Session = Depends(get_session)):
    return create_comment(comment, db)

@router.get("/{comment_id}", response_model=CommentRead)
def read(comment_id: int, db: Session = Depends(get_session)):
    return get_comment(comment_id, db)

@router.patch("/{comment_id}", response_model=CommentRead)
def update(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_session)):
    return update_comment(comment_id, comment_update, db)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(comment_id: int, db: Session = Depends(get_session)):
    delete_comment(comment_id, db)
