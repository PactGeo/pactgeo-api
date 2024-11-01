import json
from datetime import datetime
from slugify import slugify
from sqlmodel import Session, select
from fastapi import HTTPException, status
from api.public.debate.models import Debate, DebateCreate, DebateUpdate, DebateRead, DebateType, DebateChangeLog
from api.public.country.models import Country
from api.public.user.models import User
from api.public.tag.models import Tag
from api.public.point_of_view.models import PointOfView, Opinion, OpinionCreate
from sqlalchemy.orm import joinedload, selectinload

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
    debate = db.exec(
        select(Debate)
        .where(Debate.slug == slug)
        .options(
            selectinload(Debate.creator),
            selectinload(Debate.points_of_view).options(
                selectinload(PointOfView.opinions).options(
                    selectinload(Opinion.user),
                    selectinload(Opinion.votes)
                )
            )
        )
    ).first()
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

def create_debate(debate: DebateCreate, db: Session, current_user: User) -> Debate:
    slug = generate_slug(debate.title, db)
    db_debate = Debate(
        title=debate.title,
        slug=slug,
        description=debate.description,
        type=debate.type,
        public=debate.public,
        status=debate.status,
        language=debate.language,
        creator_id=current_user.id,
        images=debate.images
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

def add_opinion_to_debate(debate_id: int, opinion_create: OpinionCreate, db: Session, user: User):
    print("=== add_opinion_to_debate ===: ")
    print("debate_id: ", debate_id)
    print("opinion_create: ", opinion_create)
    print("user: ", user)
    
    content = opinion_create.content
    country_name = opinion_create.country

    country_id = None
    if country_name:
        country = db.exec(select(Country).where(Country.name == country_name)).first()
        if not country:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El país especificado no existe.")
        country_id = country.id

    # Obtener el debate
    debate = db.get(Debate, debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate no encontrado")

    if debate.type in [DebateType.GLOBAL, DebateType.INTERNATIONAL]:
        print("debate.type: ", debate.type)
        # do something
    else:
        country_id = None

    # Verificar si el punto de vista ya existe
    statement = select(PointOfView).where(
        PointOfView.debate_id == debate_id,
        PointOfView.country_id == country_id,
    )
    point_of_view = db.exec(statement).first()

    # Si no existe, crearlo
    if not point_of_view:
        point_of_view = PointOfView(
            debate_id=debate_id,
            name=country_name,
            country_id=country_id,
            created_by_id=user.id
        )
        db.add(point_of_view)
        db.commit()
        db.refresh(point_of_view)

    # Verificar si el usuario ya comentó en este punto de vista
    statement = select(Opinion).where(
        Opinion.point_of_view_id == point_of_view.id,
        Opinion.user_id == user.id
    )
    existing_comment = db.exec(statement).first()
    if existing_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya has comentado en este punto de vista")

    # Crear el comentario
    opinion = Opinion(
        point_of_view_id=point_of_view.id,
        user_id=user.id,
        content=content
    )
    db.add(opinion)
    db.commit()
    db.refresh(opinion)

    return opinion

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
