from sqlmodel import Session, select
from fastapi import HTTPException, status
from api.public.tag.models import Tag, TagCreate, TagUpdate
from api.public.debate.models import Debate

def create_tag(tag: TagCreate, session: Session) -> Tag:
    db_tag = Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

def get_tag(*, session: Session, tag_id: int) -> Tag:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

def get_all_tags(db: Session) -> list[Tag]:
    results = db.exec(select(Tag))
    return results

def update_tag(*, session: Session, tag_id: int, tag_update: TagUpdate) -> Tag:
    db_tag = get_tag(session=session, tag_id=tag_id)
    tag_data = tag_update.dict(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

def delete_tag(*, session: Session, tag_id: int) -> None:
    tag = get_tag(session=session, tag_id=tag_id)
    session.delete(tag)
    session.commit()
