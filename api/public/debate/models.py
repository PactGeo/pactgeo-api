from typing import Optional
from datetime import datetime
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel
from api.public.tag.models import Tag
from api.public.user.models import User
from api.public.debate_tag_link.models import DebateTagLink

class DebateBase(SQLModel):
    type: str
    title: str = Field(index=True)
    description: Optional[str] = None
    image_url: Optional[str] = None
    public: bool = True
    status: Optional[str] = None
    views_count: int = 0
    likes_count: int = 0
    dislikes_count: int = 0
    comments_count: int = 0
    points_of_view_count: int = 0
    is_featured: bool = False
    is_locked: bool = False
    last_comment_at: Optional[datetime] = None
    is_flagged: bool = False
    moderator_notes: Optional[str] = None
    locked_by: Optional[int] = None
    archived_at: Optional[datetime] = None
    language: Optional[str] = None
    min_characters_per_comment: int = 0
    max_characters_per_comment: int = 0

class Debate(DebateBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="user.id")
    community_id: int = Field(foreign_key="community.id")
    
    creator: User | None = Relationship(back_populates="debates")
    comments: list["Comment"] = Relationship(back_populates="debate")
    tags: list["Tag"] = Relationship(back_populates="debates", link_model=DebateTagLink)
    
class DebateCreate(DebateBase):
    community_id: int
    creator_id: int
    type: str
    tags: list[str] = []

class DebateRead(DebateBase):
    id: int
    title: str
    description: Optional[str]
    public: bool
    creator_id: int
    creator_username: Optional[str] = None
    community_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: list[str] = []

    @field_validator("tags", mode="before")
    def get_tag_names(cls, value):
        # Extrae el nombre de cada objeto Tag
        return [tag.name if isinstance(tag, Tag) else tag for tag in value]

class DebateUpdate(DebateBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
