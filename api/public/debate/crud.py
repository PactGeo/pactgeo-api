from sqlmodel import Session, select
from fastapi import HTTPException, status
from api.public.debate.models import Debate, DebateCreate, DebateUpdate, DebateRead
from api.public.tag.models import Tag
from api.public.user.models import User

def create_debate(debate: DebateCreate, db: Session) -> Debate:
    # db_debate = Debate.model_validate(debate)
    db_debate = Debate(
        type=debate.type,
        title=debate.title,
        description=debate.description,
        image_url=debate.image_url,
        public=debate.public,
        status=debate.status,
        views_count=debate.views_count,
        likes_count=debate.likes_count,
        dislikes_count=debate.dislikes_count,
        comments_count=debate.comments_count,
        points_of_view_count=debate.points_of_view_count,
        is_featured=debate.is_featured,
        is_locked=debate.is_locked,
        last_comment_at=debate.last_comment_at,
        is_flagged=debate.is_flagged,
        moderator_notes=debate.moderator_notes,
        locked_by=debate.locked_by,
        archived_at=debate.archived_at,
        language=debate.language,
        min_characters_per_comment=debate.min_characters_per_comment,
        max_characters_per_comment=debate.max_characters_per_comment,
        creator_id=debate.creator_id,
        community_id=debate.community_id
    )
    
    
    # Find or create tags and associate them with the debate
    tags = []
    for tag_name in debate.tags:
        tag = db.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            # Create the tag if it does not exist
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)

    db_debate.tags = tags  # Assigning tags found or created to the discussion
    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)
    return db_debate

def get_all_debates(db: Session) -> list[Debate]:
    results = db.exec(select(Debate))
    return results

def get_debate(debate_id: int, db: Session) -> Debate:
    debate = db.get(Debate, debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")
    return debate

def get_debates_by_type(debate_type: str, db: Session) -> list[Debate]:
    # Realiza un join entre Debate y User para obtener el username del creador
    # global_debates = select(Debate)
    statement = select(Debate, User.username).join(User, Debate.creator_id == User.id).where(Debate.type == debate_type)
    results = db.exec(statement)

    # Crea una lista de debates con el username del creador
    debates = []
    for debate, username in results:
        debate_data = DebateRead.model_validate(debate)
        debate_data.creator_username = username  # Asigna el username al modelo
        debates.append(debate_data)

    return debates

def get_global_debates(db: Session) -> list[Debate]:
    return get_debates_by_type("global", db)

def get_international_debates(db: Session) -> list[Debate]:
    return get_debates_by_type("international", db)

def get_national_debates(db: Session) -> list[Debate]:
    return get_debates_by_type("national", db)

def get_local_debates(db: Session) -> list[Debate]:
    return get_debates_by_type("local", db)

def update_debate(debate_id: int, debate_update: DebateUpdate, db: Session) -> Debate:
    debate = db.get(Debate, debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")
    debate_data = debate_update.dict(exclude_unset=True)
    for key, value in debate_data.items():
        setattr(debate, key, value)
    db.add(debate)
    db.commit()
    db.refresh(debate)
    return debate

def delete_debate(debate_id: int, db: Session) -> None:
    debate = db.get(Debate, debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")
    db.delete(debate)
    db.commit()
