from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from api.utils.generic_models import DebateTagLink, PollTagLink

class TagBase(SQLModel):
    name: str = Field(..., max_length=50)

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    polls: list["Poll"] = Relationship(back_populates="tags", link_model=PollTagLink)
    debates: list["Debate"] = Relationship(back_populates="tags", link_model=DebateTagLink)

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int

class TagUpdate(TagBase):
    pass
