from sqlmodel import Session
from fastapi import HTTPException, status
from api.public.comment.models import Comment, CommentCreate, CommentUpdate

def create_comment(comment: CommentCreate, db: Session) -> Comment:
    db_comment = Comment.model_validate(comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(comment_id: int, db: Session) -> Comment:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session) -> Comment:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comment_data = comment_update.dict(exclude_unset=True)
    for key, value in comment_data.items():
        setattr(comment, key, value)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(comment_id: int, db: Session) -> None:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    db.delete(comment)
    db.commit()
