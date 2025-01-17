# models.py

from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLAlchemyEnum, UniqueConstraint
from pydantic import ConfigDict
from api.public.tag.models import Tag
from api.utils.generic_models import PollTagLink, PollCommunityLink
from api.public.community.models import CommunityRead

# Enums
class PollType(str, Enum):
    BINARY = 'BINARY'
    SINGLE_CHOICE = 'SINGLE_CHOICE'
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'

class PollStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    DRAFT = 'DRAFT'

class ReactionType(str, Enum):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'

# Base Models
class PollBase(SQLModel):
    title: str = Field(max_length=100, index=True)
    description: Optional[str] = None
    poll_type: PollType
    is_anonymous: bool = True
    ends_at: Optional[datetime] = None
    scope: Optional[str] = Field(default=None)


class Poll(PollBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    creator_id: int = Field(foreign_key="users.id")
    status: PollStatus = Field(
        default=PollStatus.ACTIVE,
        sa_column=Column(
            SQLAlchemyEnum(PollStatus),
            nullable=False
        )
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    communities: list["Community"] = Relationship(back_populates="polls", link_model=PollCommunityLink)
    tags: list[Tag] = Relationship(back_populates="polls", link_model=PollTagLink)
    creator: Optional["User"] = Relationship(back_populates="polls")
    options: list["PollOption"] = Relationship(back_populates="poll", cascade_delete=True)
    votes: list["Vote"] = Relationship(back_populates="poll")
    reactions: list["PollReaction"] = Relationship(back_populates="poll")
    comments: list["PollComment"] = Relationship(back_populates="poll")

    @property
    def creator_username(self):
        return self.creator.username if self.creator else None
    @property
    def likes_count(self) -> int:
        if self.reactions:
            return sum(1 for reaction in self.reactions if reaction.reaction_type == ReactionType.LIKE)
        return 0
    @property
    def dislikes_count(self) -> int:
        if self.reactions:
            return sum(1 for reaction in self.reactions if reaction.reaction_type == ReactionType.DISLIKE)
        return 0
    @property
    def comments_count(self) -> int:
        return len(self.comments) if self.comments else 0

class PollCreate(PollBase):
    title: str
    description: Optional[str] = None
    poll_type: PollType
    is_anonymous: bool = True
    ends_at: Optional[datetime] = None
    status: PollStatus = PollStatus.ACTIVE
    options: list[str]
    tags: list[str] = []
    scope: Optional[str] = None
    community_ids: list[int]
class PollOption(SQLModel, table=True):
    __tablename__ = "poll_options"
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    votes: int = Field(default=0)
    poll_id: int = Field(foreign_key="poll.id")

    poll: Optional[Poll] = Relationship(back_populates="options")
    votes_rel: list["Vote"] = Relationship(back_populates="option")

class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: int = Field(foreign_key="poll.id")
    option_id: int = Field(foreign_key="poll_options.id")
    user_id: int = Field(foreign_key="users.id")
    voted_at: datetime = Field(default_factory=datetime.utcnow)

    poll: Optional[Poll] = Relationship(back_populates="votes")
    option: Optional[PollOption] = Relationship(back_populates="votes_rel")
    user: Optional["User"] = Relationship(back_populates="poll_votes")

# Pydantic Models for Validation and Response
class PollOptionCreate(SQLModel):
    text: str

class PollUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[PollStatus] = None
    ends_at: Optional[datetime] = None

class PollOptionRead(SQLModel):
    id: int
    poll_id: int
    text: str
    votes: int
    model_config = ConfigDict(from_attributes=True)

class CommentRead(SQLModel):
    id: int
    poll_id: int
    user_id: int
    username: str
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PollRead(PollBase):
    id: int
    slug: str
    title: str
    description: Optional[str] = None
    poll_type: PollType
    is_anonymous: bool
    status: PollStatus
    created_at: datetime
    updated_at: datetime
    ends_at: Optional[datetime] = None
    tags: list[str] = []
    creator_id: int
    creator_username: str
    communities: list[CommunityRead] = []
    options: list[PollOptionRead]
    likes_count: int
    dislikes_count: int
    user_voted_options: list[int] = []
    user_reaction_type: Optional[ReactionType] = None
    comments_count: int
    comments: list[CommentRead] = []
    community_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_poll(cls, poll: "Poll") -> "PollRead":
        return cls(
            id=poll.id,
            slug=poll.slug,
            title=poll.title,
            description=poll.description,
            poll_type=poll.poll_type,
            is_anonymous=poll.is_anonymous,
            status=poll.status,
            created_at=poll.created_at,
            updated_at=poll.updated_at,
            ends_at=poll.ends_at,
            tags=[tag.name for tag in poll.tags],
            creator_id=poll.creator_id,
            creator_username=poll.creator.username if poll.creator else "Unknown",
            communities=[CommunityRead.model_validate(community) for community in poll.communities],
            community_ids=[community.id for community in poll.communities],
            scope=poll.scope,
            options=[PollOptionRead.model_validate(option) for option in poll.options],
            likes_count=poll.likes_count,
            dislikes_count=poll.dislikes_count,
            user_voted_options=[],
            user_reaction_type=None,
            comments_count=poll.comments_count,
            comments=[CommentRead.model_validate(comment) for comment in poll.comments]
        )

class VoteRequest(SQLModel):
    option_ids: list[int]

class PollOptionResult(SQLModel):
    option_id: int
    text: str
    votes: int
    percentage: float

class PollResults(SQLModel):
    poll_id: int
    title: str
    description: Optional[str]
    total_votes: int
    options: list[PollOptionResult]

class PollReaction(SQLModel, table=True):
    __tablename__ = "poll_reactions"
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: int = Field(foreign_key="poll.id")
    user_id: int = Field(foreign_key="users.id")
    reaction_type: ReactionType
    reacted_at: datetime = Field(default_factory=datetime.utcnow)

    poll: Optional[Poll] = Relationship(back_populates="reactions")
    user: Optional["User"] = Relationship(back_populates="poll_reactions")

    __table_args__ = (
        UniqueConstraint('poll_id', 'user_id', name='_user_poll_reaction_uc'),
    )

class PollComment(SQLModel, table=True):
    __tablename__ = "poll_comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: int = Field(foreign_key="poll.id")
    user_id: int = Field(foreign_key="users.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    poll: Optional[Poll] = Relationship(back_populates="comments")
    user: Optional["User"] = Relationship(back_populates="poll_comments")

class CommentCreate(SQLModel):
    content: str

class ReactionRequest(SQLModel):
    reaction_type: ReactionType