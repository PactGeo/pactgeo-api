from datetime import datetime
from typing import Optional
from slugify import slugify
from sqlmodel import Session, select
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload, selectinload
from api.public.poll.models import (
    Poll,
    PollCreate,
    PollUpdate,
    PollRead,
    PollType,
    PollStatus,
    PollOption,
    PollOptionRead,
    VoteRequest,
    PollResults,
    PollOptionResult,
    Vote,
    PollReaction,
    PollComment,
    CommentCreate,
    CommentRead,
    ReactionRequest,
    ReactionType
)
from api.public.user.models import User
from api.public.tag.models import Tag

def generate_slug(title: str, db: Session) -> str:
    slug_base = slugify(title)
    # Verify if the slug already exists
    slug = slug_base
    counter = 1
    while db.exec(select(Poll).where(Poll.slug == slug)).first():
        slug = f"{slug_base}-{counter}"
        counter += 1
    return slug

def get_all_polls(tags: Optional[list[str]], db: Session, current_user: Optional[User]) -> list[PollRead]:
    query = select(Poll).options(
        joinedload(Poll.creator),
        selectinload(Poll.options),
        selectinload(Poll.reactions),
        selectinload(Poll.comments).joinedload(PollComment.user),
        selectinload(Poll.tags)
    )
    if tags:
        query = query.where(Poll.tags.any(Tag.name.in_(tags)))
    polls = db.exec(query).all()
    poll_reads = []
    if current_user:
        poll_ids = [poll.id for poll in polls]
        user_votes = db.exec(
            select(Vote)
            .where(Vote.poll_id.in_(poll_ids), Vote.user_id == current_user.id)
        ).all()
        votes_by_poll = {}
        for vote in user_votes:
            votes_by_poll.setdefault(vote.poll_id, []).append(vote.option_id)
        user_reactions = db.exec(
            select(PollReaction)
            .where(PollReaction.poll_id.in_(poll_ids), PollReaction.user_id == current_user.id)
        ).all()
        reactions_by_poll = {reaction.poll_id: reaction.reaction_type for reaction in user_reactions}
    else:
        votes_by_poll = {}
        reactions_by_poll = {}
    for poll in polls:
        likes = sum(1 for reaction in poll.reactions if reaction.reaction_type == ReactionType.LIKE)
        dislikes = sum(1 for reaction in poll.reactions if reaction.reaction_type == ReactionType.DISLIKE)
        user_voted_option_ids = votes_by_poll.get(poll.id, [])
        user_reaction_type = reactions_by_poll.get(poll.id)
        comments_count = len(poll.comments) if poll.comments else 0

        comments = [
            CommentRead(
                id=comment.id,
                poll_id=comment.poll_id,
                user_id=comment.user_id,
                username=comment.user.username if comment.user else "Unknown",
                content=comment.content,
                created_at=comment.created_at
            )
            for comment in poll.comments
        ]

        try:
            tags = [tag.name for tag in poll.tags]

            poll_dict = {
                "id": poll.id,
                "slug": poll.slug,
                "title": poll.title,
                "description": poll.description,
                "poll_type": poll.poll_type,
                "is_anonymous": poll.is_anonymous,
                "status": poll.status,
                "created_at": poll.created_at,
                "updated_at": poll.updated_at,
                "ends_at": poll.ends_at,
                "tags": tags,
                "creator_id": poll.creator_id,
                "creator_username": poll.creator.username if poll.creator else "",
                "community_id": poll.community_id,
                "options": [
                    PollOptionRead(
                        id=option.id,
                        poll_id=option.poll_id,
                        text=option.text,
                        votes=option.votes
                    ) for option in poll.options
                ],
                "likes_count": likes,
                "dislikes_count": dislikes,
                "user_voted_options": user_voted_option_ids,
                "user_reaction_type": user_reaction_type,
                "comments_count": comments_count,
                "comments": comments
            }

            poll_read = PollRead.model_validate(poll_dict)
            poll_reads.append(poll_read)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar la encuesta con ID {poll.id}: {str(e)}"
            )
    
    return poll_reads

def get_polls_by_community(community_id: int, tags: Optional[list[str]], db: Session, current_user: Optional[User]) -> list[PollRead]:
    query = select(Poll).options(
        joinedload(Poll.creator),
        selectinload(Poll.options),
        selectinload(Poll.reactions),
        selectinload(Poll.comments),
        selectinload(Poll.tags)
    ).where(Poll.community_id == community_id)
    if tags:
        query = query.where(Poll.tags.any(Tag.name.in_(tags)))
    polls = db.exec(query).all()
    poll_reads = []
    if current_user:
        poll_ids = [poll.id for poll in polls]
        user_votes = db.exec(
            select(Vote)
            .where(Vote.poll_id.in_(poll_ids), Vote.user_id == current_user.id)
        ).all()
        votes_by_poll = {}
        for vote in user_votes:
            votes_by_poll.setdefault(vote.poll_id, []).append(vote.option_id)
        user_reactions = db.exec(
            select(PollReaction)
            .where(PollReaction.poll_id.in_(poll_ids), PollReaction.user_id == current_user.id)
        ).all()
        reactions_by_poll = {reaction.poll_id: reaction.reaction_type for reaction in user_reactions}
    else:
        votes_by_poll = {}
        reactions_by_poll = {}
    
    for poll in polls:
        likes = sum(1 for reaction in poll.reactions if reaction.reaction_type == ReactionType.LIKE)
        dislikes = sum(1 for reaction in poll.reactions if reaction.reaction_type == ReactionType.DISLIKE)
        user_voted_option_ids = votes_by_poll.get(poll.id, [])
        user_reaction_type = reactions_by_poll.get(poll.id)
        comments_count = len(poll.comments) if poll.comments else 0

        comments = [
            CommentRead(
                id=comment.id,
                poll_id=comment.poll_id,
                user_id=comment.user_id,
                username=comment.user.username if comment.user else "Unknown",
                content=comment.content,
                created_at=comment.created_at
            )
            for comment in poll.comments
        ]
        
        try:
            tags = [tag.name for tag in poll.tags]
            poll_dict = {
                "id": poll.id,
                "slug": poll.slug,
                "title": poll.title,
                "description": poll.description,
                "poll_type": poll.poll_type,
                "is_anonymous": poll.is_anonymous,
                "status": poll.status,
                "created_at": poll.created_at,
                "updated_at": poll.updated_at,
                "ends_at": poll.ends_at,
                "tags": tags,
                "creator_id": poll.creator_id,
                "creator_username": poll.creator.username if poll.creator else "",
                "community_id": poll.community_id,
                "options": [
                    PollOptionRead(
                        id=option.id,
                        poll_id=option.poll_id,
                        text=option.text,
                        votes=option.votes
                    ) for option in poll.options
                ],
                "likes_count": likes,
                "dislikes_count": dislikes,
                "user_voted_options": user_voted_option_ids,
                "user_reaction_type": user_reaction_type,
                "comments_count": comments_count,
                "comments": comments
            }
            poll_read = PollRead.model_validate(poll_dict)
            poll_reads.append(poll_read)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar la encuesta con ID {poll.id}: {str(e)}"
            )
    
    return poll_reads

def get_poll(slug: str, db: Session) -> PollRead:
    poll = db.exec(
        select(Poll)
        .options(joinedload(Poll.options))
        .where(Poll.slug == slug)
    ).first()
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")
    db.refresh(poll)
    # username = poll.creator.username if poll.creator else "Unknown"
    return []

def create_poll(poll: PollCreate, db: Session, current_user: User) -> Poll:
    print('poll')
    print(poll)
    print('hola')
    slug = generate_slug(poll.title, db)
    print('slug')
    print(slug)
    
    db_poll = Poll(
        title=poll.title,
        slug=slug,
        description=poll.description,
        poll_type=poll.poll_type,
        is_anonymous=poll.is_anonymous,
        ends_at=poll.ends_at,
        status=poll.status,
        community_id=poll.community_id,
        creator_id=current_user.id,
    )
    print('db_poll')
    print(db_poll)

    # Create the poll options
    if len(poll.options) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requieren al menos dos opciones")
    
    db_options = []
    for option_text in poll.options:
        db_option = PollOption(text=option_text)
        db_options.append(db_option)
    db_poll.options = db_options

    if poll.tags:
        existing_tags = db.exec(
            select(Tag).where(Tag.name.in_(poll.tags))
        ).all()
        
        # Verify if all the sent tags exist
        missing_tags = set(poll.tags) - {tag.name for tag in existing_tags}
        if missing_tags:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The following tags do not exist: {', '.join(missing_tags)}"
            )
        
        db_poll.tags = existing_tags

    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    return db_poll

def update_poll(
    poll_id: int,
    poll_update: PollUpdate,
    db: Session,
    current_user: User
) -> Poll:
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    # Verificar si el usuario tiene permiso para actualizar la encuesta
    if poll.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

    # Registro de cambios (opcional)
    change_logs = []

    for key, value in poll_update.dict(exclude_unset=True).items():
        old_value = getattr(poll, key)
        if old_value != value:
            setattr(poll, key, value)
            # Si deseas implementar un registro de cambios, puedes hacerlo aquí

    poll.updated_at = datetime.utcnow()

    db.add(poll)
    db.commit()
    db.refresh(poll)
    return poll

def delete_poll(poll_id: int, db: Session, current_user: User) -> None:
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    # Verificar si el usuario tiene permiso para eliminar la encuesta
    if poll.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

    db.delete(poll)
    db.commit()

def vote_in_poll(
    poll_id: int,
    vote_request: VoteRequest,
    db: Session,
    current_user: User
) -> dict:
    print(1)
    poll = db.exec(
        select(Poll)
        .options(joinedload(Poll.options))
        .where(Poll.id == poll_id)
    ).first()
    print(2)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    # Verify if the poll is active
    print(3)
    if poll.status != PollStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Poll is not active")

    # Verify if the poll has expired
    print(4)
    if poll.ends_at and poll.ends_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Poll has expired")

    # Get the existing votes of the user in this poll
    print(5)
    existing_votes = db.exec(
        select(Vote)
        .where(Vote.poll_id == poll_id, Vote.user_id == current_user.id)
    ).all()
    print(6)
    existing_option_ids = {vote.option_id for vote in existing_votes}

    selected_option_ids = set(vote_request.option_ids)

    # Validating that the selected options belong to the poll
    poll_option_ids = {option.id for option in poll.options}
    invalid_option_ids = selected_option_ids - poll_option_ids
    if invalid_option_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid option IDs: {invalid_option_ids}")

    if poll.poll_type in [PollType.BINARY, PollType.SINGLE_CHOICE]:
        # Solo se permite una opción
        if len(selected_option_ids) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one option can be selected in this poll")

        selected_option_id = next(iter(selected_option_ids), None)
        if selected_option_id in existing_option_ids:
            # Cancel the existing vote
            vote_to_delete = next(vote for vote in existing_votes if vote.option_id == selected_option_id)
            db.delete(vote_to_delete)
            # Disminuir el conteo de votos en la opción
            option = db.get(PollOption, selected_option_id)
            option.votes -= 1
            db.add(option)
            db.commit()
            updated_options = db.exec(
                select(PollOption)
                .where(PollOption.poll_id == poll_id)
            ).all()

            # Serialize the options to return them
            options_data = [
                {
                    "id": option.id,
                    "text": option.text,
                    "votes": option.votes
                }
                for option in updated_options
            ]
            return {
                "detail": "Vote canceled successfully",
                "options": options_data
            }
        else:
            # Change the vote
            # Eliminar el voto anterior si existe
            for vote in existing_votes:
                db.delete(vote)
                option = db.get(PollOption, vote.option_id)
                option.votes -= 1
                db.add(option)
            # Añadir el nuevo voto
            new_vote = Vote(
                poll_id=poll_id,
                option_id=selected_option_id,
                user_id=current_user.id
            )
            db.add(new_vote)
            option = db.get(PollOption, selected_option_id)
            option.votes += 1
            db.add(option)
            db.commit()
            updated_options = db.exec(
                select(PollOption)
                .where(PollOption.poll_id == poll_id)
            ).all()

            # Serialize the options to return them
            options_data = [
                {
                    "id": option.id,
                    "text": option.text,
                    "votes": option.votes
                }
                for option in updated_options
            ]
            return {
                "detail": "Vote updated successfully",
                "options": options_data
            }
    elif poll.poll_type == PollType.MULTIPLE_CHOICE:
        # Procesar cada opción seleccionada
        for option_id in poll_option_ids:
            if option_id in selected_option_ids and option_id not in existing_option_ids:
                # Nuevo voto
                new_vote = Vote(
                    poll_id=poll_id,
                    option_id=option_id,
                    user_id=current_user.id
                )
                db.add(new_vote)
                option = db.get(PollOption, option_id)
                option.votes += 1
                db.add(option)
            elif option_id not in selected_option_ids and option_id in existing_option_ids:
                # Cancelar voto existente
                vote_to_delete = next(vote for vote in existing_votes if vote.option_id == option_id)
                db.delete(vote_to_delete)
                option = db.get(PollOption, option_id)
                option.votes -= 1
                db.add(option)
        db.commit()
        return {"detail": "Votes updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid poll type")

def get_poll_results(poll_id: int, db: Session) -> PollResults:
    poll = db.exec(
        select(Poll)
        .options(joinedload(Poll.options))
        .where(Poll.id == poll_id)
    ).first()
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    total_votes = sum(option.votes for option in poll.options)
    options_results = []
    for option in poll.options:
        percentage = (option.votes / total_votes * 100) if total_votes > 0 else 0
        option_result = PollOptionResult(
            option_id=option.id,
            text=option.text,
            votes=option.votes,
            percentage=round(percentage, 2)
        )
        options_results.append(option_result)

    poll_results = PollResults(
        poll_id=poll.id,
        title=poll.title,
        description=poll.description,
        total_votes=total_votes,
        options=options_results
    )
    return poll_results

def close_poll(
    poll_id: int,
    db: Session,
    current_user: User
) -> dict:
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    # Verificar si el usuario tiene permiso para cerrar la encuesta
    if poll.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

    poll.status = "closed"
    db.add(poll)
    db.commit()
    return {"detail": "Poll closed successfully"}

def react_to_poll(
    poll_id: int,
    reaction_request: ReactionRequest,
    db: Session,
    current_user: User
) -> dict:
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    existing_reaction = db.exec(
        select(PollReaction)
        .where(PollReaction.poll_id == poll_id, PollReaction.user_id == current_user.id)
    ).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_request.reaction_type:
            # Cancel the reaction
            db.delete(existing_reaction)
            db.commit()
            return {"detail": "Reaction canceled successfully"}
        else:
            # Update the reaction
            existing_reaction.reaction_type = reaction_request.reaction_type
            existing_reaction.reacted_at = datetime.utcnow()
            db.add(existing_reaction)
            db.commit()
            return {"detail": "Reaction updated successfully"}
    else:
        # Add a new reaction
        new_reaction = PollReaction(
            poll_id=poll_id,
            user_id=current_user.id,
            reaction_type=reaction_request.reaction_type
        )
        db.add(new_reaction)
        db.commit()
        return {"detail": "Reaction recorded successfully"}

def add_comment_to_poll(
    poll_id: int,
    comment_request: CommentCreate,
    db: Session,
    current_user: User
) -> CommentRead:
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    comment = PollComment(
        poll_id=poll_id,
        user_id=current_user.id,
        content=comment_request.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return CommentRead(
        id=comment.id,
        poll_id=comment.poll_id,
        user_id=comment.user_id,
        username=current_user.username,
        content=comment.content,
        created_at=comment.created_at
    )

def get_comments_for_poll(poll_id: int, db: Session) -> list[CommentRead]:
    comments = db.exec(
        select(PollComment)
        .options(joinedload(PollComment.user))
        .where(PollComment.poll_id == poll_id)
        .order_by(PollComment.created_at.asc())
    ).all()
    return [
        CommentRead(
            id=comment.id,
            poll_id=comment.poll_id,
            user_id=comment.user_id,
            username=comment.user.username,
            content=comment.content,
            created_at=comment.created_at
        ) for comment in comments
    ]
