from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from api.public.user.crud import create_user, get_user_by_username, update_user, delete_user
from api.public.user.models import User, UserCreate, UserRead, UserUpdate, UserReadWithCounts
from api.database import get_session
from api.public.dependencies import get_optional_current_user
from api.utils.generic_models import UserFollowLink

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(user, db)

@router.get("/me", response_model=UserRead)
def read_me(db: Session = Depends(get_session), current_user: Optional[User] = Depends(get_optional_current_user)):
    return current_user
    # return get_me(db, current_user)

@router.patch("/me", response_model=UserRead)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_optional_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return update_user(current_user.id, user_update, db)


@router.get("/{username}", response_model=UserReadWithCounts)
def read_by_username(username: str, db: Session = Depends(get_session)):
    return get_user_by_username(username, db)

@router.patch("/{user_id}", response_model=UserRead)
def update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    return update_user(user_id, user_update, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_session)):
    delete_user(user_id, db)

@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def follow_user(user_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    statement = select(UserFollowLink).where(
        UserFollowLink.follower_id == current_user.id,
        UserFollowLink.followed_id == user_id
    )
    existing_follow = db.exec(statement).first()

    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")

    # Verificar que el usuario a seguir exista
    followed_user = db.get(User, user_id)
    if not followed_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_follow = UserFollowLink(follower_id=current_user.id, followed_id=user_id)
    db.add(new_follow)
    db.commit()
    return

@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(user_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    statement = select(UserFollowLink).where(
        UserFollowLink.follower_id == current_user.id,
        UserFollowLink.followed_id == user_id
    )
    existing_follow = db.exec(statement).first()

    if not existing_follow:
        raise HTTPException(status_code=400, detail="You are not following this user")

    db.delete(existing_follow)
    db.commit()
    return
