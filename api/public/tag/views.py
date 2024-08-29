from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from api.public.tag.models import TagRead, TagCreate, TagUpdate
from api.public.tag.crud import create_tag, get_tag, get_all_tags, update_tag, delete_tag
from api.database import get_session

router = APIRouter()

@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_new_tag(*, session: Session = Depends(get_session), tag: TagCreate):
    return create_tag(session=session, tag=tag)

@router.get("/{tag_id}", response_model=TagRead)
def read_tag(*, session: Session = Depends(get_session), tag_id: int):
    return get_tag(session=session, tag_id=tag_id)

@router.get("/", response_model=list[TagRead])
def read_all_tags(db: Session = Depends(get_session)):
    return get_all_tags(db)

@router.patch("/{tag_id}", response_model=TagRead)
def update_existing_tag(*, session: Session = Depends(get_session), tag_id: int, tag_update: TagUpdate):
    return update_tag(session=session, tag_id=tag_id, tag_update=tag_update)

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_tag(*, session: Session = Depends(get_session), tag_id: int):
    delete_tag(session=session, tag_id=tag_id)
