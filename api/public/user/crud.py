from sqlmodel import Session, select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from api.public.user.models import User, UserCreate, UserUpdate, UserReadWithCounts

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(user: UserCreate, db: Session):
    db_user = User.model_validate(user)
    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        role=user.role,
        is_active=user.is_active,
        birthdate=user.birthdate,
        image=user.image,
        gender=user.gender,
        country_id=user.country_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_me(db: Session, current_user: User) -> User:
    return current_user

def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

def get_user_by_username(username: str, db: Session) -> UserReadWithCounts:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    followers_count = len(user.followers)
    following_count = len(user.following)

    return UserReadWithCounts(**user.__dict__, followers_count=followers_count, following_count=following_count)

def update_user(user_id: int, user_update: UserUpdate, db: Session) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session) -> None:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(user)
    db.commit()
