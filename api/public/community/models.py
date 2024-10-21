from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from api.utils.generic_models import UserCommunityLink

if TYPE_CHECKING:
    from api.public.user.models import User
    from api.public.poll.models import Poll

class CommunityBase(SQLModel):
    name: str
    type: str
    description: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="communities.id")

class Community(CommunityBase, table=True):
    __tablename__ = "communities"
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
        back_populates="community"
    )

class CommunityCreate(CommunityBase):
    pass

class CommunityRead(CommunityBase):
    id: int

class CommunityUpdate(CommunityBase):
    pass
