from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from api.public.debate.models import Debate
from api.public.user.models import User

class CommentBase(SQLModel):
    content: str

class Comment(CommentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    debate_id: Optional[int] = Field(default=None, foreign_key="debate.id")
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    debate: Optional["Debate"] = Relationship(back_populates="comments")
    creator: Optional["User"] = Relationship(back_populates="comments")

class CommentCreate(CommentBase):
    debate_id: int

class CommentRead(CommentBase):
    id: int
    debate_id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class CommentUpdate(CommentBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
