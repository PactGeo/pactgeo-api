from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import ConfigDict
from api.public.subdivision.models import Subdivision
from api.public.user.models import UserPublic

class PointOfView(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True)
    debate_id: int = Field(foreign_key="debate.id", description="Foreign key to the parent debate")
    name: str = Field(description="Name of the point of view (e.g., country, province)")
    country_id: Optional[int] = Field(default=None, foreign_key="country.id", description="Foreign key to the parent country")
    subnation_id: Optional[int] = Field(default=None, foreign_key="subnation.id", description="Foreign key to the parent subnation")
    subdivision_id: Optional[int] = Field(default=None, foreign_key="subdivision.id", description="Foreign key to the parent subdivision")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time of creation")
    created_by_id: int = Field(foreign_key="users.id", description="Foreign key to the user who created the point of view")
    
    # Relations
    debate: Optional["Debate"] = Relationship(back_populates="points_of_view")
    opinions: list["Opinion"] = Relationship(back_populates="point_of_view")
    country: Optional["Country"] = Relationship(back_populates="points_of_view")
    subnation: Optional["Subnation"] = Relationship(back_populates="points_of_view")
    subdivision: Optional["Subdivision"] = Relationship(back_populates="points_of_view")

class PointOfViewRead(SQLModel):
    id: int
    name: str
    debate_id: int
    country_id: Optional[int]
    subnation_id: Optional[int]
    subdivision_id: Optional[int]
    created_at: datetime
    created_by_id: int
    opinions: list["OpinionRead"] = []
    model_config = ConfigDict(from_attributes=True)

class Opinion(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True)
    point_of_view_id: int = Field(foreign_key="pointofview.id", description="Foreign key to the parent point of view")
    user_id: int = Field(foreign_key="users.id", description="Foreign key to the user who created the opinion")
    content: str = Field(max_length=5000, description="Content of the opinion")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time of creation")

    # Relations
    point_of_view: Optional["PointOfView"] = Relationship(back_populates="opinions")
    votes: list["OpinionVote"] = Relationship(back_populates="opinion")
    user: Optional["User"] = Relationship(back_populates="opinions")

class OpinionRead(SQLModel):
    id: int
    point_of_view_id: int
    content: str
    created_at: datetime
    user: UserPublic
    upvotes: int
    downvotes: int
    score: int
    model_config = ConfigDict(from_attributes=True)
    
class OpinionCreate(SQLModel):
    content: str
    country: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Esta es mi opinión sobre el debate.",
                "country": "Argentina"
            }
        }

class OpinionVote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    opinion_id: int = Field(foreign_key="opinion.id")
    user_id: int = Field(foreign_key="users.id")
    value: int = Field(description="Valor del voto: 1 para 'up', -1 para 'down'")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    opinion: "Opinion" = Relationship(back_populates="votes")
    user: "User" = Relationship(back_populates="opinion_votes")

class OpinionVoteCreate(SQLModel):
    value: int

    class Config:
        json_schema_extra = {
            "example": {
                "value": 1
            }
        }