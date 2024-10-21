from enum import Enum
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from api.public.tag.models import Tag
from api.public.country.models import Country
from api.public.subnation.models import Subnation
from api.public.user.models import User
from api.utils.generic_models import DebateTagLink
from api.utils.generic_models import DebateCountryInvolvedLink, DebateSubnationInvolvedLink
from api.public.point_of_view.models import PointOfView
from sqlalchemy import Column, JSON, BigInteger

class DebateType(str, Enum):
    GLOBAL = "GLOBAL"
    INTERNATIONAL = "INTERNATIONAL"
    NATIONAL = "NATIONAL"
    SUBNATIONAL = "SUBNATIONAL"
    SUBDIVISION = "SUBDIVISION"
class DebateStatus(str, Enum):
    OPEN = "OPEN"
    PENDING = "PENDING"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    RESOLVED = "RESOLVED"
class LanguageCode(str, Enum):
    EN = "en"
    ES = "es"
    FR = "fr"
    
# Base model with common fields for Debate
class DebateBase(SQLModel):
    description: Optional[str] = Field(default=None, description="Description of the debate")
    dislikes_count: int = Field(default=0, ge=0, sa_column=Column(BigInteger), description="Number of dislikes of the debate")
    images: list[str] = Field(default_factory=list, sa_column=Column(JSON), description="List of image URLs")
    language: Optional[LanguageCode] = Field(default=LanguageCode.EN, description="Language code of the debate")
    likes_count: int = Field(default=0, ge=0, sa_column=Column(BigInteger), description="Number of likes of the debate")
    public: bool = Field(default=True, description="If the debate is public or private")
    slug: Optional[str] = Field(default=None, unique=True, index=True, description="Slug for the debate, generated from the title")
    status: DebateStatus = Field(default=DebateStatus.OPEN, description="Status of the debate")
    title: str = Field(index=True, min_length=5, max_length=100, description="Title of the debate")
    type: DebateType = Field(description="Type of debate: GLOBAL, INTERNATIONAL, NATIONAL, SUBNATIONAL, SUBDIVISION")
    views_count: int = Field(default=0, ge=0, description="Number of views of the debate")
    views_count: int = Field(default=0, ge=0, sa_column=Column(BigInteger), description="Number of views of the debate")


# Main Debate model, representing the debate table in the database
class Debate(DebateBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the debate was created", index=True)
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when the debate was last updated")
    deleted_at: Optional[datetime] = Field(default=None, description="Timestamp when the debate was deleted")
    creator_id: int = Field(foreign_key="users.id")
    approved_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    rejected_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    approved_at: Optional[datetime] = Field(default=None)
    rejected_at: Optional[datetime] = Field(default=None)

    # Relationships
    # creator: Optional[User] = Relationship(back_populates="debates_created")
    # approved_by: Optional[User] = Relationship(back_populates="debates_approved")
    # rejected_by: Optional[User] = Relationship(back_populates="debates_rejected")
    creator: Optional["User"] = Relationship(
        back_populates="debates_created",
        sa_relationship_kwargs={"foreign_keys": "[Debate.creator_id]"}
    )
    approved_by: Optional["User"] = Relationship(
        back_populates="debates_approved",
        sa_relationship_kwargs={"foreign_keys": "[Debate.approved_by_id]"}
    )
    rejected_by: Optional["User"] = Relationship(
        back_populates="debates_rejected",
        sa_relationship_kwargs={"foreign_keys": "[Debate.rejected_by_id]"}
    )
    tags: list[Tag] = Relationship(back_populates="debates", link_model=DebateTagLink)
    countries_involved: list[Country] = Relationship(back_populates="debates", link_model=DebateCountryInvolvedLink)
    subnations_involved: list[Subnation] = Relationship(back_populates="debates", link_model=DebateSubnationInvolvedLink)
    points_of_view: list["PointOfView"] = Relationship(back_populates="debate")
    moderation_notes: Optional[str] = Field(default=None, description="Notes from the moderator")

    change_logs: list["DebateChangeLog"] = Relationship(back_populates="debate")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "creator_id": 1,
                "title": "Is climate change real?",
                "description": "A debate about climate change",
                "public": True,
                "type": "GLOBAL",
                "tags": ["climate", "change", "global"],
                "created_at": "2021-08-01T12:00:00",
                "updated_at": "2021-08-01T12:00:00",
                "deleted_at": None,
                "views_count": 0,
                "likes_count": 0,
                "dislikes_count": 0,
                "language": "en",
                "status": "open"
            }
        }

# Create model for creating a new debate
class DebateCreate(DebateBase):
    creator_id: int
    type: DebateType
    tags: list[str] = []
    images: list[str] = []
    countries_involved: list[str] = []
    subnations_involved: list[str] = []

# Read model for reading debates, defines which fields are exposed in the API
class DebateRead(DebateBase):
    id: int
    creator_id: int
    creator_username: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    tags: list[str] = []
    countries_involved: list[str] = []
    subnations_involved: list[str] = []
    points_of_view: list[PointOfView] = []
    images: list[str]

    @classmethod
    def from_debate(cls, debate: Debate, username: str) -> "DebateRead":
        return cls(
            id=debate.id,
            title=debate.title,
            slug=debate.slug,
            description=debate.description,
            public=debate.public,
            creator_id=debate.creator_id,
            creator_username=username,
            type=debate.type,
            tags=[tag.name for tag in debate.tags],
            countries_involved=[country_involved.name for country_involved in debate.countries_involved],
            subnations_involved=[subnation_involved.name for subnation_involved in debate.subnations_involved],
            created_at=debate.created_at,
            updated_at=debate.updated_at,
            deleted_at=debate.deleted_at,
            views_count=debate.views_count,
            likes_count=debate.likes_count,
            dislikes_count=debate.dislikes_count,
            language=debate.language,
            status=debate.status,
            images=debate.get_images()
        )

# Update model for updating an existing debate
class DebateUpdate(DebateBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    

class DebateChangeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    debate_id: int = Field(foreign_key="debate.id")
    changed_by_id: int = Field(foreign_key="users.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: Optional[str] = None

    debate: Optional["Debate"] = Relationship(back_populates="change_logs")
    changed_by: Optional[User] = Relationship()
