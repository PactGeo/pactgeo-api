from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from api.public.poll.crud import (
    create_poll,
    get_poll,
    update_poll,
    delete_poll,
    get_polls_by_community,
    get_all_polls,
    vote_in_poll,
    get_poll_results,
    close_poll,
    react_to_poll,
    add_comment_to_poll,
    get_comments_for_poll,
)
from api.public.poll.models import (
    PollCreate,
    PollRead,
    PollUpdate,
    VoteRequest,
    PollResults,
    ReactionRequest,
    CommentCreate,
    CommentRead,
)
from api.database import get_session
from api.public.dependencies import get_current_user, get_optional_current_user
from api.public.user.models import User

router = APIRouter()

@router.get("/", response_model=List[PollRead])
def read_polls(
    community_id: Optional[int] = Query(None, description="ID of the community to filter polls"),
    db: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    if community_id:
        return get_polls_by_community(community_id, db, current_user)
    return get_all_polls(db, current_user)

@router.get("/{poll_id}", response_model=PollRead)
def read_poll(poll_id: int, db: Session = Depends(get_session)):
    return get_poll(poll_id, db)

@router.post("/", response_model=PollRead, status_code=status.HTTP_201_CREATED)
def create(
    poll: PollCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    print('############################################ POLL ############################################')
    print(poll)
    return create_poll(poll, db, current_user)

@router.patch("/{poll_id}", response_model=PollRead)
def update(
    poll_id: int, poll_update: PollUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return update_poll(poll_id, poll_update, db, current_user)

@router.delete("/{poll_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(poll_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    delete_poll(poll_id, db, current_user)
    return {"detail": "Poll deleted successfully"}

@router.post("/{poll_id}/vote", status_code=status.HTTP_200_OK)
def vote(
    poll_id: int,
    vote_request: VoteRequest,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    print('############################################ VOTE ############################################')
    print(vote_request)
    return vote_in_poll(poll_id, vote_request, db, current_user)

@router.get("/{poll_id}/results", response_model=PollResults)
def results(poll_id: int, db: Session = Depends(get_session)):
    return get_poll_results(poll_id, db)

@router.post("/{poll_id}/close", status_code=status.HTTP_200_OK)
def close(poll_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return close_poll(poll_id, db, current_user)

@router.post("/{poll_id}/react", status_code=status.HTTP_200_OK)
def react(
    poll_id: int,
    reaction_request: ReactionRequest,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return react_to_poll(poll_id, reaction_request, db, current_user)

@router.post("/{poll_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def add_comment(
    poll_id: int,
    comment_request: CommentCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return add_comment_to_poll(poll_id, comment_request, db, current_user)

@router.get("/{poll_id}/comments", response_model=List[CommentRead])
def read_comments(
    poll_id: int,
    db: Session = Depends(get_session)
):
    return get_comments_for_poll(poll_id, db)
