# models.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from api.utils.generic_models import DebateCountryInvolvedLink
from api.public.continent.models import Continent

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Official name of the country")
    area: Optional[float] = Field(default=None, description="Total area in square kilometers")
    borders: Optional[str] = Field(default=None, description="Countries that share a border with this country")
    capital_latlng: Optional[str] = Field(default=None, description="Coordinates of the capital city")
    capital: Optional[str] = Field(default=None, description="Capital city of the country")
    cca2: Optional[str] = Field(default=None, index=True, description="ISO alpha-2 country code")
    cca3: Optional[str] = Field(default=None, index=True, description="ISO alpha-3 country code")
    coat_of_arms_svg: Optional[str] = Field(default=None, description="URL to SVG image of the coat of arms")
    continent: Optional[str] = Field(default=None, description="Continent the country belongs to")
    currency_code: Optional[str] = Field(default=None, description="ISO code of the currency")
    currency_name: Optional[str] = Field(default=None, description="Name of the currency")
    flag: Optional[str] = Field(default=None, description="Emoji representing the country flag")
    google_maps_link: Optional[str] = Field(default=None, description="Google Maps link of the country")
    idd_root: Optional[str] = Field(default=None, description="International direct dialing root code")
    idd_suffixes: Optional[str] = Field(default=None, description="International direct dialing suffixes")
    landlocked: Optional[bool] = Field(default=None, description="Whether the country is landlocked or not")
    languages: Optional[str] = Field(default=None, description="Official languages of the country")
    native_name: Optional[str] = Field(default=None, description="Native names of the country in official languages")
    numeric_code: Optional[str] = Field(default=None, description="ISO numeric country code")
    openstreet_maps_link: Optional[str] = Field(default=None, description="OpenStreetMap link of the country")
    population: Optional[int] = Field(default=None, description="Total population of the country")
    region: Optional[str] = Field(default=None, description="Geographical region of the country")
    status: Optional[str] = Field(default=None, description="Official assignment status of the country")
    subregion: Optional[str] = Field(default=None, description="Specific subregion of the country")
    timezone: Optional[str] = Field(default=None, description="Primary time zone of the country")

    continent_id: Optional[int] = Field(default=None, foreign_key="continent.id", description="Foreign key to the parent continent")
    
    # Relationship
    continent: Optional["Continent"] = Relationship(back_populates="countries")
    subnations: list["Subnation"] = Relationship(back_populates="country")
    debates: list["Debate"] = Relationship(back_populates="countries_involved", link_model=DebateCountryInvolvedLink)
    points_of_view: list["PointOfView"] = Relationship(back_populates="country")
