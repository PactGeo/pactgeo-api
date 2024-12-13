from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from api.utils.generic_models import UserFollowLink, UserCommunityLink
from api.public.community.models import Community

class UserRole(str, Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'

class UserBase(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50, unique=True)
    email: str = Field(max_length=100, unique=True)
    name: Optional[str] = Field(default=None, max_length=50)
    emailVerified: Optional[datetime] = None
    banner: Optional[str] = None
    image: Optional[str] = None
    birthdate: Optional[datetime] = None
    gender: Optional[str] = Field(default=None, max_length=20)
    bio: Optional[str] = Field(default=None, max_length=240)
    location: Optional[str] = Field(default=None, max_length=40)
    website: Optional[str] = Field(default=None, max_length=100)
    isActive: Optional[bool] = None
    role: Optional[UserRole] = None
    country_id: Optional[int] = Field(default=None, foreign_key="country.id")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    communities: List[Community] = Relationship(
        back_populates="users",
        link_model=UserCommunityLink
    )
    accounts: list["Accounts"] = Relationship(back_populates="user")
    opinions: list["Opinion"] = Relationship(back_populates="user")
    opinion_votes: list["OpinionVote"] = Relationship(back_populates="user")
    polls: list["Poll"] = Relationship(back_populates="creator")
    poll_votes: list["Vote"] = Relationship(back_populates="user")
    poll_reactions: list["PollReaction"] = Relationship(back_populates="user")
    poll_comments: list["PollComment"] = Relationship(back_populates="user")

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=True)
    updated_at: Optional[datetime] = Field(default=None)

    debates_created: list["Debate"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == Debate.creator_id",
            "foreign_keys": "[Debate.creator_id]"
        }
    )
    debates_approved: list["Debate"] = Relationship(
        back_populates="approved_by",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == Debate.approved_by_id",
            "foreign_keys": "[Debate.approved_by_id]"
        }
    )
    debates_rejected: list["Debate"] = Relationship(
        back_populates="rejected_by",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == Debate.rejected_by_id",
            "foreign_keys": "[Debate.rejected_by_id]"
        }
    )

    followers: list["User"] = Relationship(
        back_populates="following",
        link_model=UserFollowLink,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == UserFollowLink.followed_id",
            "secondaryjoin": "User.id == UserFollowLink.follower_id",
        }
    )
    following: list["User"] = Relationship(
        back_populates="followers",
        link_model=UserFollowLink,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == UserFollowLink.follower_id",
            "secondaryjoin": "User.id == UserFollowLink.followed_id",
        }
    )


class UserCreate(UserBase):
    country_id: Optional[int] = None

class UserRead(UserBase):
    id: int
    username: str
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserReadWithCounts(UserRead):
    followers_count: int
    following_count: int

class UserPublic(SQLModel):
    id: int
    username: str
    image: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    emailVerified: Optional[datetime] = None
    banner: Optional[str] = None
    image: Optional[str] = Field(None, max_length=100)
    birthdate: Optional[datetime] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    isActive: Optional[bool] = None
    role: Optional[UserRole] = None
    country_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Accounts(SQLModel, table=True):
    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    type: str
    provider: str
    provider_account_id: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_at: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    session_state: Optional[str] = None

    user: "User" = Relationship(back_populates="accounts")
