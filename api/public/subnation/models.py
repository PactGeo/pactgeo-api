# models.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from api.utils.generic_models import DebateSubnationInvolvedLink

class Subnation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Official name of the subnation")
    area: Optional[float] = Field(default=None, description="Total area in square kilometers")
    population: Optional[int] = Field(default=None, description="Total population of the subnation")
    borders: Optional[str] = Field(default=None, description="Subnations that share a border with this subnation")
    capital: Optional[str] = Field(default=None, description="Capital city of the subnation")
    flag: Optional[str] = Field(default=None, description="URL to SVG image of the subnation flag")
    iso_code: Optional[str] = Field(default=None, description="ISO code of the subnation")
    timezone: Optional[str] = Field(default=None, description="Primary time zone of the subnation")
    famous_landmark: Optional[str] = Field(default=None, description="Famous landmark in the subnation")

    country_id: Optional[int] = Field(default=None, foreign_key="country.id", description="Foreign key to the parent country")
    country: Optional["Country"] = Relationship(back_populates="subnations")

    debates: list["Debate"] = Relationship(back_populates="subnations_involved", link_model=DebateSubnationInvolvedLink)
    subdivisions: list["Subdivision"] = Relationship(back_populates="subnation")
    points_of_view: list["PointOfView"] = Relationship(back_populates="subnation")