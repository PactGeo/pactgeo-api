from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from api.public.usercommunitylink.models import UserCommunityLink  # Importar la clase

class CommunityBase(SQLModel):
    name: str
    type: str
    description: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="community.id")  # Clave foránea a la misma tabla

class Community(CommunityBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    users: list["User"] = Relationship(back_populates="communities", link_model=UserCommunityLink)  # Usar la clase, no un string

    parent: Optional["Community"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Community.id"}
    )

class CommunityCreate(CommunityBase):
    pass

class CommunityRead(CommunityBase):
    id: int

class CommunityUpdate(CommunityBase):
    pass
