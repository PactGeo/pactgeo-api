import json
from slugify import slugify
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException, status
from api.public.debate.models import Debate, DebateCreate, DebateUpdate, DebateRead, DebateType, DebateChangeLog
from api.public.country.models import Country
from api.public.user.models import User
from api.public.tag.models import Tag
from sqlalchemy.orm import joinedload

def generate_slug(title: str, db: Session) -> str:
    slug_base = slugify(title)
    # Verify if the slug already exists
    slug = slug_base
    counter = 1
    while db.exec(select(Debate).where(Debate.slug == slug)).first():
        slug = f"{slug_base}-{counter}"
        counter += 1
    return slug

def get_all_debates(db: Session) -> list[DebateRead]:
    debates = db.exec(select(Debate)).all()
    return [DebateRead.from_debate(debate) for debate in debates]

def get_debate(slug: str, db: Session) -> DebateRead:
    debate = db.exec(select(Debate).where(Debate.slug == slug)).first()
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")
    db.refresh(debate)
    username = debate.creator.username if debate.creator else "Unknown"
    return DebateRead.from_debate(debate, username)

def get_debates_by_type(debate_type: str, db: Session) -> list[DebateRead]:
    debates = db.exec(
        select(Debate)
        .options(joinedload(Debate.creator))
        .where(Debate.type == debate_type)
    ).all()
    print("===DEBATES===: ", debates)
    return [
        DebateRead.from_debate(debate, debate.creator.username if debate.creator else "Unknown")
        for debate in debates
    ]

def create_debate(debate: DebateCreate, db: Session) -> Debate:
    slug = generate_slug(debate.title, db)
    print("======SLUG======: ", slug)
    db_debate = Debate(
        title=debate.title,
        slug=slug,
        description=debate.description,
        type=debate.type,
        public=debate.public,
        status=debate.status,
        language=debate.language,
        creator_id=debate.creator_id,
        images=json.dumps(debate.images)
    )

    if debate.tags:
        tags = db.exec(select(Tag).where(Tag.name.in_(debate.tags))).all()
        if len(tags) != len(debate.tags):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some tags do not exist")
        db_debate.tags = tags   

    if debate.type == DebateType.INTERNATIONAL and hasattr(debate, 'countries_involved'):
        countries = db.exec(select(Country).where(Country.name.in_(debate.countries_involved))).all()
        db_debate.countries_involved = countries

    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)

    return db_debate

def update_debate(
    debate_id: int,
    debate_update: DebateUpdate,
    db: Session,
    current_user: User
) -> Debate:
    debate = db.get(Debate, debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")

    # Verificar si el usuario tiene permiso para actualizar el debate
    if debate.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

    # Registro de cambios
    change_logs = []

    for key, value in debate_update.dict(exclude_unset=True).items():
        old_value = getattr(debate, key)
        if old_value != value:
            setattr(debate, key, value)
            change_log = DebateChangeLog(
                debate_id=debate.id,
                changed_by_id=current_user.id,
                changed_at=datetime.utcnow(),
                field_changed=key,
                old_value=json.dumps(old_value) if isinstance(old_value, (dict, list)) else str(old_value),
                new_value=json.dumps(value) if isinstance(value, (dict, list)) else str(value),
                reason="User update"
            )
            change_logs.append(change_log)

    debate.updated_at = datetime.utcnow()

    db.add_all(change_logs)
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
