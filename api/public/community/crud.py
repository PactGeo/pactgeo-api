from sqlmodel import Session
from fastapi import HTTPException, status
from api.public.community.models import Community, CommunityCreate, CommunityUpdate


def create_community(community: CommunityCreate, db: Session) -> Community:
    db_community = Community.model_validate(community)
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community


def get_community(community_id: int, db: Session) -> Community:
    community = db.get(Community, community_id)
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Community not found"
        )
    return community


def update_community(
    community_id: int, community_update: CommunityUpdate, db: Session
) -> Community:
    community = db.get(Community, community_id)
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Community not found"
        )
    community_data = community_update.dict(exclude_unset=True)
    for key, value in community_data.items():
        setattr(community, key, value)
    db.add(community)
    db.commit()
    db.refresh(community)
    return community


def delete_community(community_id: int, db: Session) -> None:
    community = db.get(Community, community_id)
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Community not found"
        )
    db.delete(community)
    db.commit()
