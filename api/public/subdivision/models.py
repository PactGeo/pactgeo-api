from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Subdivision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Official name of the subdivision")
    area: Optional[float] = Field(default=None, description="Total area in square kilometers")
    population: Optional[int] = Field(default=None, description="Total population of the subdivision")
    borders: Optional[str] = Field(default=None, description="Subdivisions that share a border with this subdivision")
    iso_code: Optional[str] = Field(default=None, description="ISO code of the subdivision")
    timezone: Optional[str] = Field(default=None, description="Primary time zone of the subdivision")
    famous_landmark: Optional[str] = Field(default=None, description="Famous landmark in the subdivision")

    subnation_id: Optional[int] = Field(default=None, foreign_key="subnation.id", description="Foreign key to the parent subnation")
    country_id: Optional[int] = Field(default=None, foreign_key="country.id", description="Foreign key to the parent country")

    subnation: Optional["Subnation"] = Relationship(back_populates="subdivisions")
    points_of_view: list["PointOfView"] = Relationship(back_populates="subdivision")