from typing import Optional
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from api.utils.generic_models import UserCommunityLink, PollCommunityLink

class CommunityLevel(str, Enum):
    GLOBAL = 'GLOBAL'
    CONTINENT = 'CONTINENT'
    NATIONAL = 'NATIONAL'
    SUBNATIONAL = 'SUBNATIONAL'
    LOCAL = 'LOCAL'

class CommunityBase(SQLModel):
    name: str
    level: CommunityLevel = Field(default=CommunityLevel.GLOBAL)
    description: Optional[str] = None

    parent_id: Optional[int] = Field(default=None, foreign_key="community.id")

class Community(CommunityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relaciones
    users: list["User"] = Relationship(
        back_populates="communities",
        link_model=UserCommunityLink
    )

    parent: Optional["Community"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Community.id"},
        back_populates="children"
    )

    children: list["Community"] = Relationship(
        back_populates="parent"
    )

    polls: list["Poll"] = Relationship(
        back_populates="communities",
        link_model=PollCommunityLink
    )

class CommunityCreate(CommunityBase):
    pass

class CommunityRead(CommunityBase):
    id: int

class CommunityUpdate(CommunityBase):
    pass
