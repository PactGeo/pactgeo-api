from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from api.utils.generic_models import UserCommunityLink


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class UserBase(SQLModel):
    username: Optional[str] = Field(
        max_length=50,
        regex=r"^[a-zA-Z0-9_]+$",
        index=True,
        unique=True,
        nullable=True
    )
    email: str = Field(
        max_length=100,
        regex=r"^\S+@\S+\.\S+$",
        unique=True,
        index=True,
    )
    name: Optional[str] = Field(None, max_length=100)
    emailVerified: Optional[datetime] = None
    image: Optional[str] = Field(
        None,
        regex=r"^https?:\/\/.*\.(?:png|jpg|jpeg|gif|svg)$",
        nullable=True
    )
    birthdate: Optional[datetime] = None
    gender: Optional[str] = Field(None, max_length=20, nullable=True)
    isActive: bool = Field(default=True, nullable=True)
    role: UserRole = Field(default=UserRole.USER, nullable=True)
    
class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    country_id: Optional[int] = Field(foreign_key="country.id")

    #Relations
    accounts: list["Accounts"] = Relationship(back_populates="user")
    opinion_votes: list["OpinionVote"] = Relationship(back_populates="user")
    polls: list["Poll"] = Relationship(back_populates="creator")
    poll_votes: list["Vote"] = Relationship(back_populates="user")
    poll_reactions: list["PollReaction"] = Relationship(back_populates="user")
    poll_comments: list["PollComment"] = Relationship(back_populates="user")
    opinions: list["Opinion"] = Relationship(back_populates="user")

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=True)
    updated_at: Optional[datetime] = Field(default=None)

    # debates_created: list["Debate"] = Relationship(back_populates="creator")
    # debates_approved: list["Debate"] = Relationship(back_populates="approved_by")
    # debates_rejected: list["Debate"] = Relationship(back_populates="rejected_by")

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

    communities: list["Community"] = Relationship(back_populates="users", link_model=UserCommunityLink)

class UserCreate(UserBase):
    country_id: Optional[int] = None


class UserRead(UserBase):
    id: int
    username: str
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserPublic(SQLModel):
    id: int
    username: str
    image: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    image: Optional[str] = Field(None, max_length=100)

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
