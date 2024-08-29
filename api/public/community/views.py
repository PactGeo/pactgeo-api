from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from api.public.community.crud import (
    create_community,
    get_community,
    update_community,
    delete_community,
)
from api.public.community.models import CommunityCreate, CommunityRead, CommunityUpdate
from api.database import get_session

router = APIRouter()


@router.post("/", response_model=CommunityRead, status_code=status.HTTP_201_CREATED)
def create(community: CommunityCreate, db: Session = Depends(get_session)):
    return create_community(community, db)


@router.get("/{community_id}", response_model=CommunityRead)
def read(community_id: int, db: Session = Depends(get_session)):
    return get_community(community_id, db)


@router.patch("/{community_id}", response_model=CommunityRead)
def update(
    community_id: int,
    community_update: CommunityUpdate,
    db: Session = Depends(get_session),
):
    return update_community(community_id, community_update, db)


@router.delete("/{community_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(community_id: int, db: Session = Depends(get_session)):
    delete_community(community_id, db)
