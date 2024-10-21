# api/public/globalcommunity/models.py
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.public.continent.models import Continent

class GlobalCommunity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="Global", description="Name of the global community")
    description: Optional[str] = Field(default=None, description="Description of the global community")

    # Relaciones
    continents: list["Continent"] = Relationship(back_populates="global_community")
