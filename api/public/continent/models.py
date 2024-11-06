from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.public.country.models import Country

class Continent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Name of the continent")
    description: Optional[str] = Field(default=None, description="Description of the continent")

    # Relaciones
    countries: list["Country"] = Relationship(back_populates="continent")
