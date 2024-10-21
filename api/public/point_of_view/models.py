from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

# Modelo para los puntos de vista del debate
class PointOfView(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True)
    name: str = Field(..., description="Name of the point of view (e.g., country, province)")
    debate_id: int = Field(foreign_key="debate.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relación con el debate
    debate: Optional["Debate"] = Relationship(back_populates="points_of_view")
    opinions: list["Opinion"] = Relationship(back_populates="point_of_view")

# Modelo para las opiniones dentro de los puntos de vista
class Opinion(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True)
    content: str = Field(..., description="Content of the opinion")
    creator_id: int = Field(foreign_key="users.id")
    point_of_view_id: int = Field(foreign_key="pointofview.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    point_of_view: Optional[PointOfView] = Relationship(back_populates="opinions")
    creator: Optional["User"] = Relationship()
