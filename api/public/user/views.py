from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from api.public.user.crud import create_user, get_user_by_username, update_user, delete_user
from api.public.user.models import User, UserCreate, UserRead, UserUpdate
from api.database import get_session
from api.public.dependencies import get_optional_current_user

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(user, db)

@router.get("/me", response_model=UserRead)
def read_me(db: Session = Depends(get_session), current_user: Optional[User] = Depends(get_optional_current_user)):
    return current_user
    # return get_me(db, current_user)

@router.get("/{username}", response_model=UserRead)
def read_by_username(username: str, db: Session = Depends(get_session)):
    return get_user_by_username(username, db)

@router.patch("/{user_id}", response_model=UserRead)
def update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    return update_user(user_id, user_update, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_session)):
    delete_user(user_id, db)
