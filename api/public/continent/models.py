# api/public/continent/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from api.public.globalcommunity.models import GlobalCommunity

if TYPE_CHECKING:
    from api.public.country.models import Country

class Continent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Name of the continent")
    description: Optional[str] = Field(default=None, description="Description of the continent")
    global_community_id: Optional[int] = Field(default=None, foreign_key="globalcommunity.id")

    # Relaciones
    global_community: Optional["GlobalCommunity"] = Relationship(back_populates="continents")
    countries: List["Country"] = Relationship(back_populates="continent")
